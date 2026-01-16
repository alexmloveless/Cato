# /web

Search the web and add results to conversation context.

## Usage

```
/web "query"                  # Use default engine (DuckDuckGo)
/web "query" duckduckgo       # Use DuckDuckGo explicitly
/web "query" google           # Use Google
/web "query" bing             # Use Bing
```

## Description

The `/web` command searches the internet for information related to your query. Search results are fetched, their content is extracted, and the information is added to the conversation context for the LLM to analyze.

**Flow:**
1. Performs search using the specified engine
2. Extracts URLs from search results
3. Scrapes content from each URL
4. Processes and cleans the content
5. Adds formatted results to conversation context

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| query | Yes | The search query (quoted) |
| engine | No | Search engine: `duckduckgo`, `google`, `bing` |

## Configuration

```yaml
web_search:
  enabled: true
  default_engine: duckduckgo
  max_results: 3
  content_threshold: 500
  timeout: 10
```

## Examples

```
/web "python async programming"
/web "latest AI news" google
/web "climate change statistics 2024"
```

## See Also

- [/url](url.md) - Fetch content from a specific URL
- [/url_store](url_store.md) - Store URL content in vector store
