"""Search provider implementations."""

from cato.providers.search.base import SearchProvider, SearchResult
from cato.providers.search.duckduckgo import DuckDuckGoProvider

__all__ = ["SearchProvider", "SearchResult", "DuckDuckGoProvider"]
