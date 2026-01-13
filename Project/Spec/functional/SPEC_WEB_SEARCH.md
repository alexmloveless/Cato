# Web Search Specification

## Overview

Web search functionality allows users to search the internet and integrate results into the conversation context. Content is fetched, processed, and made available to the LLM for analysis.

## Commands

### /web
Search the web and add results to conversation context.

```
/web "search query"                  # Use default engine
/web "search query" google           # Use Google
/web "search query" duckduckgo       # Use DuckDuckGo
/web "search query" bing             # Use Bing
```

**Flow:**
1. Perform search using specified engine
2. Extract URLs from search results
3. Scrape content from each URL
4. Process and clean content
5. Add to conversation context
6. Generate LLM response using results

### /url
Fetch and attach content from a specific URL.

```
/url https://example.com/page.html
```

**Flow:**
1. Fetch page content
2. Extract text and metadata
3. Add to conversation as user message
4. Offer to add to vector store

## Search Engines

### Supported Engines

| Engine | Key | URL Pattern |
|--------|-----|-------------|
| DuckDuckGo | duckduckgo | `https://duckduckgo.com/html/?q={query}` |
| Google | google | `https://www.google.com/search?q={query}` |
| Bing | bing | `https://www.bing.com/search?q={query}` |

Default: `duckduckgo` (configurable)

### Custom Engines
Additional engines can be configured:

```yaml
web_search:
  engines:
    duckduckgo: "https://duckduckgo.com/html/?q={query}"
    google: "https://www.google.com/search?q={query}"
    bing: "https://www.bing.com/search?q={query}"
    custom: "https://search.example.com/?q={query}"
```

## Content Processing

### Search Result Extraction
1. Parse search results page HTML
2. Extract links and titles
3. Filter to relevant results
4. Limit to `max_results` URLs

### Content Scraping
For each URL:
1. Fetch page content (HTML)
2. Parse HTML structure
3. Extract main content (skip navigation, ads, etc.)
4. Extract title and metadata

### Text Processing
1. Remove HTML tags
2. Normalize whitespace
3. Truncate to `content_threshold` words
4. Skip non-text files (PDF, images, etc.)

### Context Formatting
Results formatted for LLM:

```
Web Search Results:

Source: Example Website (https://example.com/page)
Content:
Relevant text content from the page...

Source: Another Site (https://another.com/article)
Content:
More relevant content...
```

## Configuration

### Web Search Settings
```yaml
web_search:
  enabled: true
  default_engine: duckduckgo
  content_threshold: 500
  max_results: 3
  timeout: 10
  engines:
    google: "https://www.google.com/search?q={query}"
    bing: "https://www.bing.com/search?q={query}"
    duckduckgo: "https://duckduckgo.com/html/?q={query}"
```

| Setting | Default | Description |
|---------|---------|-------------|
| enabled | true | Enable web search functionality |
| default_engine | duckduckgo | Default search engine |
| content_threshold | 500 | Maximum words per page |
| max_results | 3 | Maximum search results to process (max 10) |
| timeout | 10 | Request timeout in seconds |
| engines | (built-in) | Search engine URL patterns |

### Disabling Web Search
```yaml
web_search:
  enabled: false
```

When disabled, `/web` command returns error.

## /url Command Behavior

### Content Attachment
```
/url https://example.com/article.html
```

**Process:**
1. Fetch URL content
2. Extract title and text
3. Add as user message:
   ```
   [URL Content]
   
   --- URL: Page Title (https://example.com/article.html) ---
   Extracted page content...
   ```
4. Display success panel

### Vector Store Prompt
After attachment:
```
Would you like to also add this URL content to the vector store for future reference? (y/n)
```

If yes:
- Content chunked using configured strategy
- Added to vector store with metadata:
  - `source: url_command`
  - `url: {url}`
  - `title: {title}`

## /web Command Behavior

### Search and Context Flow
```
/web "latest AI news"
```

**Steps:**
1. Display: "Searching web for: latest AI news"
2. Perform search via default/specified engine
3. Display: "Found 3 search results, scraping content..."
4. Scrape each result URL
5. Process and format content
6. Add to chat context
7. Display: "Found 3 results for 'latest AI news'. Content added to conversation context."
8. Generate LLM response using search context

### Enhanced Response
The LLM receives a modified prompt including:
- Original user query
- Search context instruction
- Formatted search results

LLM is instructed to:
- Analyze search results
- Provide comprehensive response
- Cite sources when appropriate
- Indicate if results don't contain relevant info

### Context Storage
Search results stored in session for:
- Potential follow-up questions
- Thread continuity

## Error Handling

### Search Errors
- Empty query: "Search query cannot be empty"
- No results: "No search results found for '{query}'"
- Network error: "Web search failed: {error}"

### URL Errors
- Missing URL: "No URL specified. Usage: /url <url>"
- Multiple URLs: "Only one URL can be processed at a time"
- Invalid URL: "URL must start with http:// or https://"
- Fetch failure: "Failed to fetch content from {url}: {error}"

### Content Errors
- Non-text file: Skipped during processing
- Timeout: Request times out after configured seconds
- Parsing failure: Page content may be empty

## Rate Limiting

### Considerations
- Respect website robots.txt (implementation-dependent)
- Add delay between requests if needed
- Limit concurrent requests

### Best Practices
- Use reasonable `max_results` (3-5 recommended)
- Set appropriate `timeout` (10s default)
- `content_threshold` limits per-page text

## User Feedback

### Progress Indicators
```
/web "search query"
✅ Found 3 results for 'search query'. Content added to conversation context.
```

### Success Display
After successful search, before LLM response:
```
🔍 Using search results for context...
```

### Error Display
```
❌ Command error: Web search failed: Connection timeout
```

## Usage Examples

### Basic Search
```
/web "python async programming"
```
Searches DuckDuckGo, adds results to context.

### Specific Engine
```
/web "machine learning trends 2024" google
```
Uses Google for search.

### URL Attachment
```
/url https://docs.python.org/3/library/asyncio.html
```
Fetches and attaches specific documentation.

### Follow-up Questions
After `/web` search, ask questions about results:
```
/web "climate change statistics 2024"
What are the key findings from these results?
```
LLM uses search context to answer.
