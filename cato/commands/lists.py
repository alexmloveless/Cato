"""List management commands."""

import logging
from io import StringIO

from rich.console import Console
from rich.table import Table

from cato.commands.base import CommandContext, CommandResult
from cato.commands.registry import command
from cato.core.types import ListItem
from cato.services.lists import ListService

logger = logging.getLogger(__name__)


def _parse_list_flags(args: tuple[str, ...]) -> tuple[dict, list[str]]:
    """
    Parse command flags and return options dict + positional args.

    Supports both short (-p high) and long (--priority=high) forms.
    """
    options = {
        "priority": None,
        "status": ["pending", "active", "in_progress"],  # Default excludes done
        "category": None,
        "tag": None,
        "sort_by": "priority",
        "order": "asc",
        "force": False,
        "description": None,
        "add_tag": None,
        "remove_tag": None,
    }
    positional = []

    i = 0
    while i < len(args):
        arg = args[i]

        if arg.startswith("--"):
            # Long form: --priority=high
            if "=" in arg:
                key, value = arg[2:].split("=", 1)
                _apply_option(options, key, value)
                i += 1
            else:
                # Long form: --priority high
                key = arg[2:]
                if i + 1 < len(args) and not args[i + 1].startswith("-"):
                    _apply_option(options, key, args[i + 1])
                    i += 2
                else:
                    _apply_option(options, key, None)
                    i += 1

        elif arg.startswith("-") and len(arg) == 2:
            # Short form: -p high
            flag = arg[1]
            if i + 1 < len(args) and not args[i + 1].startswith("-"):
                _apply_short_option(options, flag, args[i + 1])
                i += 2
            else:
                _apply_short_option(options, flag, None)
                i += 1

        else:
            # Positional argument
            positional.append(arg)
            i += 1

    return options, positional


def _apply_option(options: dict, key: str, value: str | None) -> None:
    """Apply long option to options dict."""
    if key == "status" and value:
        if value == "all":
            options[key] = ["pending", "active", "in_progress", "done"]
        else:
            options[key] = [value]
    elif key == "force":
        options[key] = True
    elif key in options and value:
        options[key] = value


def _apply_short_option(options: dict, flag: str, value: str | None) -> None:
    """Apply short flag to options dict."""
    flag_map = {
        "s": "sort_by",
        "o": "order",
        "S": "status",
        "p": "priority",
        "c": "category",
        "t": "tag",
        "d": "description",
        "f": "force",
        "T": "add_tag",
        "R": "remove_tag",
    }

    key = flag_map.get(flag)
    if key:
        if key == "status" and value:
            if value == "all":
                options[key] = ["pending", "active", "in_progress", "done"]
            else:
                options[key] = [value]
        elif key == "force":
            options[key] = True
        elif value:
            options[key] = value


def _format_status(status: str) -> str:
    """Format status as emoji."""
    status_map = {
        "pending": "⚪",
        "active": "🔵",
        "in_progress": "🟡",
        "done": "✅",
    }
    return status_map.get(status, "❓")


def _format_priority(priority: str) -> str:
    """Format priority as emoji + text."""
    priority_map = {
        "urgent": "🔥 URG",
        "high": "⚡ HIGH",
        "medium": "● MED",
        "low": "○ LOW",
    }
    return priority_map.get(priority, priority)


def format_items_table(
    items: list[ListItem],
    list_name: str | None = None,
    sort_by: str = "priority",
) -> str:
    """
    Format items as Rich table.

    Parameters
    ----------
    items : list[ListItem]
        Items to display.
    list_name : str | None
        List name for title (None for multi-list view).
    sort_by : str
        Sort field (for title display).

    Returns
    -------
    str
        Rendered table string.
    """
    title = f"List: {list_name}" if list_name else "All Lists"
    title += f" ({len(items)} items) - sorted by {sort_by}"

    table = Table(title=title)
    table.add_column("ID", width=5)
    table.add_column("S", width=3)
    table.add_column("Priority", width=10)
    table.add_column("Category", width=12)
    table.add_column("Description", width=30)
    table.add_column("Tags", width=15)

    # Add list column if showing multiple lists
    if not list_name:
        table.add_column("List", width=12, no_wrap=True)

    for item in items:
        row_data = [
            item.display_id,
            _format_status(item.status),
            _format_priority(item.priority),
            (item.category or "")[:12],
            item.description[:30],
            ",".join(item.tags[:2]) + (f"+{len(item.tags)-2}" if len(item.tags) > 2 else ""),
        ]

        if not list_name:
            row_data.append(item.list_name[:12])

        table.add_row(*row_data)

    # Render to string
    buffer = StringIO()
    console = Console(file=buffer, force_terminal=False, width=100)
    console.print(table)
    return buffer.getvalue()


@command(
    name="list",
    description="Display items in list(s)",
    usage="/list [name] [-s sort] [-o order] [-S status] [-p priority] [-c category] [-t tag]",
    aliases=["l", "ls"],
)
async def list_command(ctx: CommandContext, *args: str) -> CommandResult:
    """Display list items."""
    options, positional = _parse_list_flags(args)

    # First positional arg is list name
    list_name = positional[0] if positional else None

    # Create list service
    list_service = ListService(ctx.storage.lists, ctx.storage.list_items)

    try:
        # Get items
        items = await list_service.get_items(
            list_name=list_name,
            status=options["status"],
            priority=options["priority"],
            category=options["category"],
            tag=options["tag"],
            sort_by=options["sort_by"],
            order=options["order"],
        )

        if not items:
            return CommandResult(
                success=True,
                message="No items found matching filters."
            )

        # Format table
        table = format_items_table(items, list_name, options["sort_by"])

        return CommandResult(success=True, message=table)

    except Exception as e:
        logger.exception("Error in list command")
        return CommandResult(success=False, message=f"Error: {e}")


@command(
    name="lists",
    description="Show all lists with item counts",
    usage="/lists",
    aliases=["ll"],
)
async def lists_command(ctx: CommandContext, *args: str) -> CommandResult:
    """Show all lists with overview."""
    list_service = ListService(ctx.storage.lists, ctx.storage.list_items)

    try:
        overview = await list_service.get_list_overview()

        if not overview:
            return CommandResult(
                success=True,
                message="No lists found. Use /add to create items."
            )

        # Create table
        table = Table(title=f"All Lists ({len(overview)})")
        table.add_column("Name", width=15)
        table.add_column("Description", width=30)
        table.add_column("Total", width=8, justify="right")
        table.add_column("Pending", width=8, justify="right")
        table.add_column("Done", width=8, justify="right")

        for lst in overview:
            table.add_row(
                lst["name"],
                (lst["description"] or "")[:30],
                str(lst["total"]),
                str(lst["pending"]),
                str(lst["done"]),
            )

        # Render to string
        buffer = StringIO()
        console = Console(file=buffer, force_terminal=False, width=100)
        console.print(table)

        return CommandResult(success=True, message=buffer.getvalue())

    except Exception as e:
        logger.exception("Error in lists command")
        return CommandResult(success=False, message=f"Error: {e}")


@command(
    name="add",
    description="Add item to list",
    usage="/add <list> <description> [-p priority] [-c category] [-t tag1,tag2]",
    aliases=["a"],
)
async def add_command(ctx: CommandContext, *args: str) -> CommandResult:
    """Add item to list."""
    if len(args) < 2:
        return CommandResult(
            success=False,
            message="Usage: /add <list> <description> [-p priority] [-c category] [-t tag1,tag2]"
        )

    options, positional = _parse_list_flags(args)

    list_name = positional[0]
    description = " ".join(positional[1:])

    # Parse tags if provided
    tags = []
    if options["tag"]:
        tags = [t.strip() for t in options["tag"].split(",")]

    list_service = ListService(ctx.storage.lists, ctx.storage.list_items)

    try:
        item = await list_service.add_item(
            list_name=list_name,
            description=description,
            priority=options["priority"] or "medium",
            category=options["category"],
            tags=tags,
        )

        return CommandResult(
            success=True,
            message=f"✓ Added item #{item.display_id} to {list_name}: \"{description}\""
        )

    except Exception as e:
        logger.exception("Error in add command")
        return CommandResult(success=False, message=f"✗ Error: {e}")


@command(
    name="remove",
    description="Remove item by ID",
    usage="/remove <id>",
    aliases=["rm", "del"],
)
async def remove_command(ctx: CommandContext, *args: str) -> CommandResult:
    """Remove item by ID."""
    if not args:
        return CommandResult(
            success=False,
            message="Usage: /remove <id>"
        )

    try:
        item_id = int(args[0])
    except ValueError:
        return CommandResult(
            success=False,
            message=f"Invalid ID: {args[0]}"
        )

    list_service = ListService(ctx.storage.lists, ctx.storage.list_items)

    try:
        success, message = await list_service.remove_item(item_id)
        return CommandResult(success=success, message=f"✓ {message}" if success else f"✗ {message}")

    except Exception as e:
        logger.exception("Error in remove command")
        return CommandResult(success=False, message=f"✗ Error: {e}")


@command(
    name="update",
    description="Update item fields",
    usage="/update <id> [-d description] [-p priority] [-S status] [-c category]",
    aliases=["u", "edit"],
)
async def update_command(ctx: CommandContext, *args: str) -> CommandResult:
    """Update item fields."""
    if not args:
        return CommandResult(
            success=False,
            message="Usage: /update <id> [-d description] [-p priority] [-S status] [-c category]"
        )

    try:
        item_id = int(args[0])
    except ValueError:
        return CommandResult(
            success=False,
            message=f"Invalid ID: {args[0]}"
        )

    options, _ = _parse_list_flags(args[1:])

    # Build updates dict
    updates = {}
    if options["description"]:
        updates["description"] = options["description"]
    if options["priority"]:
        updates["priority"] = options["priority"]
    if options["status"] and len(options["status"]) == 1:
        updates["status"] = options["status"][0]
    if options["category"]:
        updates["category"] = options["category"]

    if not updates:
        return CommandResult(
            success=False,
            message="No updates specified. Use -d, -p, -S, or -c flags."
        )

    list_service = ListService(ctx.storage.lists, ctx.storage.list_items)

    try:
        success, message, _ = await list_service.update_item(item_id, **updates)
        return CommandResult(success=success, message=f"✓ {message}" if success else f"✗ {message}")

    except Exception as e:
        logger.exception("Error in update command")
        return CommandResult(success=False, message=f"✗ Error: {e}")


@command(
    name="done",
    description="Mark item as done",
    usage="/done <id>",
    aliases=["complete", "finish"],
)
async def done_command(ctx: CommandContext, *args: str) -> CommandResult:
    """Mark item as done."""
    if not args:
        return CommandResult(
            success=False,
            message="Usage: /done <id>"
        )

    try:
        item_id = int(args[0])
    except ValueError:
        return CommandResult(
            success=False,
            message=f"Invalid ID: {args[0]}"
        )

    list_service = ListService(ctx.storage.lists, ctx.storage.list_items)

    try:
        success, message, _ = await list_service.update_item(item_id, status="done")
        return CommandResult(success=success, message=f"✓ {message}" if success else f"✗ {message}")

    except Exception as e:
        logger.exception("Error in done command")
        return CommandResult(success=False, message=f"✗ Error: {e}")


@command(
    name="move",
    description="Move item to different list",
    usage="/move <id> <target_list>",
    aliases=["mv"],
)
async def move_command(ctx: CommandContext, *args: str) -> CommandResult:
    """Move item to different list."""
    if len(args) < 2:
        return CommandResult(
            success=False,
            message="Usage: /move <id> <target_list>"
        )

    try:
        item_id = int(args[0])
    except ValueError:
        return CommandResult(
            success=False,
            message=f"Invalid ID: {args[0]}"
        )

    target_list = args[1]

    list_service = ListService(ctx.storage.lists, ctx.storage.list_items)

    try:
        success, message = await list_service.move_item(item_id, target_list)
        return CommandResult(success=success, message=f"✓ {message}" if success else f"✗ {message}")

    except Exception as e:
        logger.exception("Error in move command")
        return CommandResult(success=False, message=f"✗ Error: {e}")


@command(
    name="lclear",
    description="Clear items from list",
    usage="/lclear <list> [-S status] [-f force]",
    aliases=["lclean"],
)
async def clear_command(ctx: CommandContext, *args: str) -> CommandResult:
    """Clear items from list."""
    if not args:
        return CommandResult(
            success=False,
            message="Usage: /lclear <list> [-S status] [-f force]"
        )

    options, positional = _parse_list_flags(args)
    list_name = positional[0]

    # Get single status if specified
    status = None
    if options["status"] and len(options["status"]) == 1:
        status = options["status"][0]

    list_service = ListService(ctx.storage.lists, ctx.storage.list_items)

    try:
        success, message = await list_service.clear_items(
            list_name,
            status=status,
            force=options["force"]
        )
        return CommandResult(success=success, message=f"✓ {message}" if success else f"✗ {message}")

    except Exception as e:
        logger.exception("Error in clear command")
        return CommandResult(success=False, message=f"✗ Error: {e}")


@command(
    name="delete-list",
    description="Delete entire list",
    usage="/delete-list <name> [-f force]",
    aliases=["dl", "rmlist"],
)
async def delete_list_command(ctx: CommandContext, *args: str) -> CommandResult:
    """Delete entire list."""
    if not args:
        return CommandResult(
            success=False,
            message="Usage: /delete-list <name> [-f force]"
        )

    options, positional = _parse_list_flags(args)
    list_name = positional[0]

    list_service = ListService(ctx.storage.lists, ctx.storage.list_items)

    try:
        success, message = await list_service.delete_list(list_name, force=options["force"])
        return CommandResult(success=success, message=f"✓ {message}" if success else f"✗ {message}")

    except Exception as e:
        logger.exception("Error in delete-list command")
        return CommandResult(success=False, message=f"✗ Error: {e}")
