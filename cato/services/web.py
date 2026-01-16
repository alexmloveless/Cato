"""Web search service for searching the web and fetching URL content."""

import logging
import re
from html import unescape

import httpx

from cato.core.config import WebSearchConfig
from cato.core.exceptions import NetworkError
from cato.providers.search.base import SearchProvider, SearchResult

logger = logging.getLogger(__name__)


class WebService:
    """
    Service for web search and URL content fetching.

    Coordinates between search providers and handles content formatting
    for LLM context.

    Parameters
    ----------
    search_provider : SearchProvider
        Search provider implementation.
    config : WebSearchConfig
        Web search configuration.
    """

    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    def __init__(
        self,
        search_provider: SearchProvider,
        config: WebSearchConfig,
    ) -> None:
        self._search_provider = search_provider
        self._config = config

    async def search(
        self,
        query: str,
        engine: str | None = None,
    ) -> list[SearchResult]:
        """
        Perform a web search.

        Parameters
        ----------
        query : str
            The search query string.
        engine : str | None, optional
            Search engine to use. If None, uses default provider.

        Returns
        -------
        list[SearchResult]
            List of search results with extracted content.

        Raises
        ------
        NetworkError
            If the search request fails.
        ValueError
            If an unsupported engine is specified.
        """
        if engine and engine != self._search_provider.name:
            raise ValueError(
                f"Unsupported search engine: {engine}. "
                f"Currently only '{self._search_provider.name}' is available."
            )

        max_results = min(self._config.max_results, 10)
        results = await self._search_provider.search(query, max_results=max_results)
        logger.info(f"Web search returned {len(results)} results for: {query}")
        return results

    async def fetch_url(self, url: str) -> tuple[str, str]:
        """
        Fetch content from a URL.

        Parameters
        ----------
        url : str
            The URL to fetch.

        Returns
        -------
        tuple[str, str]
            Tuple of (title, content).

        Raises
        ------
        NetworkError
            If the request fails.
        ValueError
            If the URL is invalid or content is not HTML.
        """
        try:
            async with httpx.AsyncClient(timeout=self._config.timeout) as client:
                response = await client.get(
                    url,
                    headers={"User-Agent": self.USER_AGENT},
                    follow_redirects=True,
                )
                response.raise_for_status()

                content_type = response.headers.get("content-type", "")
                if "text/html" not in content_type:
                    raise ValueError(
                        f"URL content is not HTML (content-type: {content_type})"
                    )

                html = response.text
                title = self._extract_title(html)
                content = self._extract_text_content(html)

                logger.info(f"Fetched URL content: {url} ({len(content)} chars)")
                return title, content

        except httpx.TimeoutException as e:
            logger.error(f"URL fetch timed out: {e}")
            raise NetworkError(f"Request timed out: {e}")
        except httpx.RequestError as e:
            logger.error(f"URL fetch failed: {e}")
            raise NetworkError(f"Request failed: {e}")

    def format_search_context(self, results: list[SearchResult]) -> str:
        """
        Format search results for LLM context.

        Parameters
        ----------
        results : list[SearchResult]
            Search results to format.

        Returns
        -------
        str
            Formatted context string for LLM.
        """
        if not results:
            return ""

        formatted_parts = ["Web Search Results:\n"]

        for result in results:
            formatted_parts.append(
                f"Source: {result.title} ({result.url})\n"
                f"Content:\n{result.content}\n"
            )

        return "\n".join(formatted_parts)

    def _extract_title(self, html: str) -> str:
        """
        Extract title from HTML content.

        Parameters
        ----------
        html : str
            Raw HTML content.

        Returns
        -------
        str
            Extracted title or 'Untitled'.
        """
        title_match = re.search(r"<title[^>]*>([^<]+)</title>", html, re.IGNORECASE)
        if title_match:
            title = unescape(title_match.group(1))
            return re.sub(r"\s+", " ", title).strip()
        return "Untitled"

    def _extract_text_content(self, html: str) -> str:
        """
        Extract main text content from HTML.

        Parameters
        ----------
        html : str
            Raw HTML content.

        Returns
        -------
        str
            Extracted and truncated text content.
        """
        html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL)
        html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL)
        html = re.sub(r"<nav[^>]*>.*?</nav>", "", html, flags=re.DOTALL)
        html = re.sub(r"<header[^>]*>.*?</header>", "", html, flags=re.DOTALL)
        html = re.sub(r"<footer[^>]*>.*?</footer>", "", html, flags=re.DOTALL)
        html = re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)

        text = re.sub(r"<[^>]+>", " ", html)
        text = unescape(text)
        text = re.sub(r"\s+", " ", text)
        text = text.strip()

        words = text.split()
        if len(words) > self._config.content_threshold:
            words = words[: self._config.content_threshold]
            text = " ".join(words) + "..."

        return text
