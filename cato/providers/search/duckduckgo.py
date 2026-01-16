"""DuckDuckGo search provider implementation."""

import logging
import re
from html import unescape
from urllib.parse import unquote, urlparse

import httpx

from cato.core.config import WebSearchConfig
from cato.core.exceptions import NetworkError
from cato.providers.search.base import SearchResult

logger = logging.getLogger(__name__)


class DuckDuckGoProvider:
    """
    DuckDuckGo search provider implementation.

    Uses DuckDuckGo's HTML interface to fetch search results,
    then scrapes content from each result URL.

    Parameters
    ----------
    config : WebSearchConfig
        Web search configuration.
    """

    SEARCH_URL = "https://duckduckgo.com/html/"
    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    def __init__(self, config: WebSearchConfig) -> None:
        self._config = config
        self._timeout = config.timeout
        self._content_threshold = config.content_threshold

    @property
    def name(self) -> str:
        """Provider name."""
        return "duckduckgo"

    async def search(self, query: str, max_results: int = 3) -> list[SearchResult]:
        """
        Search DuckDuckGo and extract content from results.

        Parameters
        ----------
        query : str
            The search query string.
        max_results : int, optional
            Maximum number of results to return, by default 3.

        Returns
        -------
        list[SearchResult]
            List of search results with extracted page content.

        Raises
        ------
        NetworkError
            Network request failed.
        """
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                search_results = await self._fetch_search_results(client, query)
                search_results = search_results[:max_results]

                results: list[SearchResult] = []
                for url, title, snippet in search_results:
                    content = await self._fetch_page_content(client, url)
                    results.append(
                        SearchResult(
                            url=url,
                            title=title,
                            content=content,
                            snippet=snippet,
                        )
                    )

                return results

        except httpx.TimeoutException as e:
            logger.error(f"Search request timed out: {e}")
            raise NetworkError(f"Search request timed out: {e}")
        except httpx.RequestError as e:
            logger.error(f"Search request failed: {e}")
            raise NetworkError(f"Search request failed: {e}")

    async def _fetch_search_results(
        self, client: httpx.AsyncClient, query: str
    ) -> list[tuple[str, str, str]]:
        """
        Fetch and parse DuckDuckGo search results page.

        Parameters
        ----------
        client : httpx.AsyncClient
            HTTP client to use.
        query : str
            Search query.

        Returns
        -------
        list[tuple[str, str, str]]
            List of (url, title, snippet) tuples.
        """
        response = await client.post(
            self.SEARCH_URL,
            data={"q": query},
            headers={"User-Agent": self.USER_AGENT},
        )
        response.raise_for_status()

        return self._parse_search_html(response.text)

    def _parse_search_html(self, html: str) -> list[tuple[str, str, str]]:
        """
        Parse DuckDuckGo HTML results page.

        Parameters
        ----------
        html : str
            Raw HTML content.

        Returns
        -------
        list[tuple[str, str, str]]
            List of (url, title, snippet) tuples.
        """
        results: list[tuple[str, str, str]] = []

        result_pattern = re.compile(
            r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.+?)</a>',
            re.DOTALL,
        )
        snippet_pattern = re.compile(
            r'<a[^>]+class="result__snippet"[^>]*>(.+?)</a>',
            re.DOTALL,
        )

        link_matches = result_pattern.findall(html)
        snippet_matches = snippet_pattern.findall(html)

        for i, (raw_url, raw_title) in enumerate(link_matches):
            url = self._extract_url(raw_url)
            if not url:
                continue

            title = self._strip_html(raw_title)
            snippet = ""
            if i < len(snippet_matches):
                snippet = self._strip_html(snippet_matches[i])

            results.append((url, title, snippet))

        return results

    def _extract_url(self, raw_url: str) -> str | None:
        """
        Extract actual URL from DuckDuckGo redirect URL.

        Parameters
        ----------
        raw_url : str
            Raw URL from search results (may be a redirect).

        Returns
        -------
        str | None
            Extracted URL or None if invalid.
        """
        raw_url = unescape(raw_url)

        if "uddg=" in raw_url:
            match = re.search(r"uddg=([^&]+)", raw_url)
            if match:
                return unquote(match.group(1))

        parsed = urlparse(raw_url)
        if parsed.scheme in ("http", "https"):
            return raw_url

        return None

    def _strip_html(self, text: str) -> str:
        """
        Remove HTML tags and normalize whitespace.

        Parameters
        ----------
        text : str
            Text with potential HTML tags.

        Returns
        -------
        str
            Cleaned text.
        """
        text = unescape(text)
        text = re.sub(r"<[^>]+>", "", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    async def _fetch_page_content(self, client: httpx.AsyncClient, url: str) -> str:
        """
        Fetch and extract text content from a URL.

        Parameters
        ----------
        client : httpx.AsyncClient
            HTTP client to use.
        url : str
            URL to fetch.

        Returns
        -------
        str
            Extracted text content, truncated to content_threshold words.
        """
        try:
            response = await client.get(
                url,
                headers={"User-Agent": self.USER_AGENT},
                follow_redirects=True,
            )
            response.raise_for_status()

            content_type = response.headers.get("content-type", "")
            if "text/html" not in content_type:
                return ""

            return self._extract_text_content(response.text)

        except Exception as e:
            logger.warning(f"Failed to fetch content from {url}: {e}")
            return ""

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
        if len(words) > self._content_threshold:
            words = words[: self._content_threshold]
            text = " ".join(words) + "..."

        return text
