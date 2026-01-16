# /url_store

Store previously fetched URL content in vector store.

## Usage

```
/url_store
/urlstore
```

## Description

After using `/url` to fetch content from a web page, use `/url_store` to save that content to the vector store for future reference. The content is chunked and stored with metadata including the source URL and title.

## Prerequisites

- Must have used `/url` first to fetch content
- Vector store must be enabled in configuration

## Aliases

- `/urlstore`

## Examples

```
/url https://docs.python.org/3/library/asyncio.html
/url_store
```

## Error Handling

- **No vector store**: "Vector store is not enabled. Enable it in configuration."
- **No URL content**: "No URL content found in recent conversation. Use /url first."

## See Also

- [/url](url.md) - Fetch content from a URL
- [/vadd](vadd.md) - Add text to vector store
- [/vdoc](vdoc.md) - Add document file to vector store
