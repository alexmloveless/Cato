"""Web search and URL commands."""

import logging
import re

from cato.commands.base import CommandContext, CommandResult
from cato.commands.registry import command
from cato.core.exceptions import NetworkError
from cato.providers.search import DuckDuckGoProvider
from cato.services.web import WebService
from cato.storage.vector.base import VectorDocument

logger = logging.getLogger(__name__)


def _get_web_service(ctx: CommandContext) -> WebService:
    """
    Create a WebService instance from context.

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.

    Returns
    -------
    WebService
        Configured web service.
    """
    provider = DuckDuckGoProvider(ctx.config.web_search)
    return WebService(provider, ctx.config.web_search)


def _parse_query_args(args: tuple[str, ...]) -> tuple[str, str | None]:
    """
    Parse web command arguments to extract query and optional engine.

    Parameters
    ----------
    args : tuple[str, ...]
        Command arguments.

    Returns
    -------
    tuple[str, str | None]
        Tuple of (query, engine).
    """
    if not args:
        return "", None

    full_text = " ".join(args)

    quoted_match = re.match(r'^"([^"]+)"(?:\s+(\w+))?$', full_text)
    if quoted_match:
        return quoted_match.group(1), quoted_match.group(2)

    if len(args) >= 2:
        last_arg = args[-1].lower()
        if last_arg in ("google", "duckduckgo", "bing"):
            return " ".join(args[:-1]).strip('"'), last_arg

    return full_text.strip('"'), None


@command(
    name="web",
    description="Search the web and add results to conversation context",
    usage='/web "query" [engine]',
)
async def web(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Search the web and add results to conversation context.

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
        Search query and optional engine.

    Returns
    -------
    CommandResult
        Result with success status and message.
    """
    if not ctx.config.web_search.enabled:
        return CommandResult(
            success=False,
            message="Web search is disabled. Enable it in configuration (web_search.enabled: true).",
        )

    query, engine = _parse_query_args(args)

    if not query:
        return CommandResult(
            success=False,
            message='Usage: /web "search query" [engine]',
        )

    ctx.display.show_info(f"Searching web for: {query}")

    try:
        web_service = _get_web_service(ctx)
        results = await web_service.search(query, engine=engine)

        if not results:
            return CommandResult(
                success=True,
                message=f"No search results found for '{query}'.",
            )

        formatted_context = web_service.format_search_context(results)

        ctx.conversation.add_user_message(
            f"[Web Search Context]\n\n{formatted_context}\n\n"
            f"Based on the search results above, please help me with: {query}"
        )

        ctx.display.show_info(
            f"✅ Found {len(results)} results for '{query}'. Content added to conversation context."
        )

        return CommandResult(
            success=True,
            message=f"Found {len(results)} results for '{query}'. Content added to conversation context.",
            data={"query": query, "result_count": len(results), "send_to_llm": True},
        )

    except ValueError as e:
        return CommandResult(success=False, message=str(e))
    except NetworkError as e:
        return CommandResult(success=False, message=f"Web search failed: {e}")
    except Exception as e:
        logger.error(f"Web search failed: {e}")
        return CommandResult(success=False, message=f"Web search failed: {e}")


@command(
    name="url",
    description="Fetch URL content and add to conversation",
    usage="/url <url>",
)
async def url(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Fetch URL content and add to conversation.

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
        URL to fetch.

    Returns
    -------
    CommandResult
        Result with success status and message.
    """
    if not ctx.config.web_search.enabled:
        return CommandResult(
            success=False,
            message="Web search is disabled. Enable it in configuration (web_search.enabled: true).",
        )

    if not args:
        return CommandResult(
            success=False,
            message="No URL specified. Usage: /url <url>",
        )

    if len(args) > 1:
        return CommandResult(
            success=False,
            message="Only one URL can be processed at a time.",
        )

    target_url = args[0]

    if not target_url.startswith(("http://", "https://")):
        return CommandResult(
            success=False,
            message="URL must start with http:// or https://",
        )

    try:
        web_service = _get_web_service(ctx)
        title, content = await web_service.fetch_url(target_url)

        url_message = (
            f"[URL Content]\n\n"
            f"--- URL: {title} ({target_url}) ---\n"
            f"{content}"
        )
        ctx.conversation.add_user_message(url_message)

        ctx.display.show_info(f"✅ Fetched content from: {title}")

        if ctx.vector_store:
            ctx.display.show_info(
                "Would you like to also add this URL content to the vector store "
                "for future reference? Use /url_store to add it."
            )

        return CommandResult(
            success=True,
            message=f"URL content added to conversation: {title}",
            data={
                "url": target_url,
                "title": title,
                "content_length": len(content),
                "offer_vector_store": ctx.vector_store is not None,
            },
        )

    except ValueError as e:
        return CommandResult(success=False, message=str(e))
    except NetworkError as e:
        return CommandResult(success=False, message=f"Failed to fetch content from {target_url}: {e}")
    except Exception as e:
        logger.error(f"URL fetch failed: {e}")
        return CommandResult(success=False, message=f"Failed to fetch content: {e}")


@command(
    name="url_store",
    description="Store previously fetched URL content in vector store",
    usage="/url_store",
    aliases=["urlstore"],
)
async def url_store(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Store previously fetched URL content in vector store.

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
        Unused.

    Returns
    -------
    CommandResult
        Result with success status and message.
    """
    if not ctx.vector_store:
        return CommandResult(
            success=False,
            message="Vector store is not enabled. Enable it in configuration.",
        )

    messages = ctx.conversation.to_messages()
    url_message = None
    url_info: dict[str, str] = {}

    for msg in reversed(messages):
        if msg.get("role") == "user" and msg.get("content", "").startswith("[URL Content]"):
            url_message = msg.get("content", "")
            title_match = re.search(r"--- URL: (.+?) \((.+?)\) ---", url_message)
            if title_match:
                url_info["title"] = title_match.group(1)
                url_info["url"] = title_match.group(2)
            break

    if not url_message:
        return CommandResult(
            success=False,
            message="No URL content found in recent conversation. Use /url first.",
        )

    try:
        import uuid

        doc_id = str(uuid.uuid4())[:8]
        content_start = url_message.find("---\n") + 4
        content = url_message[content_start:] if content_start > 4 else url_message

        doc = VectorDocument(
            id=doc_id,
            content=content,
            metadata={
                "type": "url_content",
                "source": "url_command",
                "url": url_info.get("url", ""),
                "title": url_info.get("title", ""),
            },
        )

        await ctx.vector_store.add([doc])

        return CommandResult(
            success=True,
            message=f"URL content added to vector store (ID: {doc_id})",
        )

    except Exception as e:
        logger.error(f"Failed to store URL content: {e}")
        return CommandResult(
            success=False,
            message=f"Failed to store URL content: {e}",
        )
