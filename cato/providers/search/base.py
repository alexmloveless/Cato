"""Search provider protocol definition."""

from dataclasses import dataclass
from typing import Protocol


@dataclass
class SearchResult:
    """
    A single web search result.

    Parameters
    ----------
    url : str
        The URL of the search result.
    title : str
        The title of the search result.
    content : str
        The extracted text content from the page.
    snippet : str
        A short snippet or description from the search results page.
    """

    url: str
    title: str
    content: str
    snippet: str


class SearchProvider(Protocol):
    """
    Protocol for web search provider implementations.

    Any class implementing these methods can be used as a search provider.
    Providers are responsible for performing web searches and extracting
    content from result pages.
    """

    @property
    def name(self) -> str:
        """
        Provider identifier.

        Returns
        -------
        str
            Provider name (e.g., 'duckduckgo', 'google', 'bing').
        """
        ...

    async def search(self, query: str, max_results: int = 3) -> list[SearchResult]:
        """
        Perform a web search and return results with extracted content.

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
        ...
