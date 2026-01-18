"""Productivity commands for task and list management."""

import logging
from datetime import datetime

from rich.table import Table

from cato.commands.base import CommandContext, CommandResult
from cato.commands.registry import command
from cato.services.productivity import ProductivityService

logger = logging.getLogger(__name__)


def _parse_task_options(args: tuple[str, ...]) -> tuple[dict, list[str]]:
    """
    Parse /st command options.
    
    Parameters
    ----------
    args : tuple[str, ...]
        Command arguments.
    
    Returns
    -------
    tuple[dict, list[str]]
        (options dict, remaining positional args).
    """
    options = {
        "sort": "created_at",
        "order": "desc",
        "priority": None,
        "category": None,
        "status": None,
    }
    positional = []
    
    i = 0
    while i < len(args):
        arg = args[i]
        
        # Long options with =
        if arg.startswith("--"):
            if "=" in arg:
                key, value = arg[2:].split("=", 1)
                if key == "sort":
                    options["sort"] = value
                elif key == "order":
                    options["order"] = value
                elif key == "priority":
                    options["priority"] = value
                elif key == "category":
                    options["category"] = value
                elif key == "status":
                    options["status"] = value
                i += 1
            else:
                # Long option with next arg as value
                key = arg[2:]
                if i + 1 < len(args) and not args[i + 1].startswith("-"):
                    value = args[i + 1]
                    if key == "sort":
                        options["sort"] = value
                    elif key == "order":
                        options["order"] = value
                    elif key == "priority":
                        options["priority"] = value
                    elif key == "category":
                        options["category"] = value
                    elif key == "status":
                        options["status"] = value
                    i += 2
                else:
                    i += 1
        # Short options
        elif arg.startswith("-") and len(arg) == 2:
            flag = arg[1]
            if i + 1 < len(args) and not args[i + 1].startswith("-"):
                value = args[i + 1]
                if flag == "s":
                    options["sort"] = value
                elif flag == "o":
                    options["order"] = value
                elif flag == "p":
                    options["priority"] = value
                elif flag == "c":
                    options["category"] = value
                elif flag == "S":
                    options["status"] = value
                i += 2
            else:
                i += 1
        else:
            # Positional argument (category filter)
            positional.append(arg)
            i += 1
    
    return options, positional


def _format_task_status(status: str) -> str:
    """
    Format task status as emoji.
    
    Parameters
    ----------
    status : str
        Task status.
    
    Returns
    -------
    str
        Status emoji.
    """
    status_map = {
        "active": "🔵",
        "in_progress": "🟡",
        "completed": "✅",
        "deleted": "🗑️",
    }
    return status_map.get(status, "⚪")


def _format_priority(priority: str | None) -> str:
    """
    Format priority as emoji and text.
    
    Parameters
    ----------
    priority : str | None
        Task priority.
    
    Returns
    -------
    str
        Formatted priority.
    """
    if not priority:
        return ""
    
    priority_map = {
        "urgent": "🔥 URGENT",
        "high": "⚡ HIGH",
        "medium": "● MED",
        "low": "○ LOW",
    }
    return priority_map.get(priority.lower(), priority)


def _format_due_date(due_date: datetime | None) -> str:
    """
    Format due date as relative string.
    
    Parameters
    ----------
    due_date : datetime | None
        Due date.
    
    Returns
    -------
    str
        Formatted date.
    """
    if not due_date:
        return ""
    
    today = datetime.now().date()
    due = due_date.date()
    
    if due == today:
        return "Today"
    elif (due - today).days == 1:
        return "Tomorrow"
    elif (due - today).days == -1:
        return "Yesterday"
    else:
        return due.strftime("%m/%d")


@command(
    name="st",
    description="Show open tasks with filtering and sorting",
    usage="/st [category] [-p priority] [-c category] [-S status] [-s sort] [-o order]",
    aliases=["show-tasks", "tasks"],
)
async def show_tasks(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Show tasks with filtering and sorting options.
    
    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
        Command arguments and options.
    
    Returns
    -------
    CommandResult
        Result with task table.
    """
    # Parse options
    options, positional = _parse_task_options(args)
    
    # Positional arg is category filter
    if positional:
        options["category"] = positional[0]
    
    # Create productivity service
    productivity = ProductivityService(ctx.storage)
    
    try:
        # Get tasks
        tasks = await productivity.get_tasks(
            category=options["category"],
            priority=options["priority"],
            status=options["status"],
            sort_by=options["sort"],
            order=options["order"],
        )
        
        if not tasks:
            return CommandResult(
                success=True,
                message="No tasks found matching filters."
            )
        
        # Create table
        table = Table(title=f"Tasks ({len(tasks)})")
        table.add_column("S", width=3)
        table.add_column("Priority", width=10)
        table.add_column("Category", width=12)
        table.add_column("ID", width=6)
        table.add_column("Task", width=30)
        table.add_column("Due", width=10)
        
        for task in tasks:
            # Extract numeric ID from full ID (assuming format like "task-001")
            task_id = task.id.split("-")[-1] if "-" in task.id else task.id[-3:]
            
            table.add_row(
                _format_task_status(task.status),
                _format_priority(task.priority),
                task.category or "",
                task_id,
                task.title[:30],
                _format_due_date(task.due_date),
            )
        
        # Render table to string
        from io import StringIO
        from rich.console import Console
        
        buffer = StringIO()
        console = Console(file=buffer, force_terminal=False, width=80)
        console.print(table)
        output = buffer.getvalue()
        
        return CommandResult(
            success=True,
            message=output
        )
    
    except Exception as e:
        logger.error(f"Failed to show tasks: {e}")
        return CommandResult(
            success=False,
            message=f"Failed to retrieve tasks: {e}"
        )



@command(
    name="addtask",
    description="Create a new task",
    usage="/addtask <title> [-p priority] [-c category] [-d description]",
    aliases=["at", "newtask"],
)
async def add_task(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Create a new task.

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
        Task title and options.

    Returns
    -------
    CommandResult
        Result with task confirmation.
    """
    if not args:
        return CommandResult(
            success=False,
            message="Usage: /addtask <title> [-p priority] [-c category] [-d description]"
        )

    # Parse options
    title_parts = []
    priority = None
    category = None
    description = None

    i = 0
    while i < len(args):
        arg = args[i]

        if arg in ["-p", "--priority"] and i + 1 < len(args):
            priority = args[i + 1]
            i += 2
        elif arg in ["-c", "--category"] and i + 1 < len(args):
            category = args[i + 1]
            i += 2
        elif arg in ["-d", "--description"] and i + 1 < len(args):
            description = args[i + 1]
            i += 2
        else:
            title_parts.append(arg)
            i += 1

    if not title_parts:
        return CommandResult(
            success=False,
            message="Task title is required."
        )

    title = " ".join(title_parts)

    # Create productivity service
    productivity = ProductivityService(ctx.storage)

    try:
        task = await productivity.create_task(
            title=title,
            description=description,
            priority=priority,
            category=category,
        )

        msg = f"✓ Created task: **{task.title}**\n"
        if priority:
            msg += f"- Priority: {priority}\n"
        if category:
            msg += f"- Category: {category}\n"
        if description:
            msg += f"- Description: {description}\n"

        return CommandResult(
            success=True,
            message=msg.strip()
        )

    except Exception as e:
        logger.error(f"Failed to create task: {e}")
        return CommandResult(
            success=False,
            message=f"Failed to create task: {e}"
        )



