# /url

Fetch content from a URL and add to conversation.

## Usage

```
/url <url>
```

## Description

The `/url` command fetches content from a specified URL, extracts the text, and adds it to the conversation context. This allows you to discuss specific web pages with the LLM.

**Flow:**
1. Validates URL (must start with `http://` or `https://`)
2. Fetches page content
3. Extracts title and text
4. Adds content as a user message
5. Optionally offers to store in vector store

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| url | Yes | The URL to fetch (must be http/https) |

## Examples

```
/url https://docs.python.org/3/library/asyncio.html
/url https://example.com/article.html
```

## Error Handling

- **Missing URL**: "No URL specified. Usage: /url <url>"
- **Multiple URLs**: "Only one URL can be processed at a time"
- **Invalid URL**: "URL must start with http:// or https://"
- **Fetch failure**: "Failed to fetch content from {url}: {error}"

## See Also

- [/web](web.md) - Search the web for information
- [/url_store](url_store.md) - Store URL content in vector store
