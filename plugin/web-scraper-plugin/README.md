# Web Scraper Plugin

A powerful, intelligent web scraping plugin for Claude Code with adaptive HTTP/browser fallback, content extraction, and automation capabilities.

## Features

### Adaptive Scraping
- **Smart Mode Selection** - Automatically chooses between HTTP and browser scraping
- **HTTP Mode** - Fast scraping for static sites using requests + BeautifulSoup
- **Browser Mode** - Handles JavaScript-heavy sites using Playwright
- **Automatic Fallback** - Falls back to browser if HTTP returns insufficient content

### Content Extraction
- **Article Extraction** - Optimized for blogs, news, and documentation
- **Product Extraction** - E-commerce product data (price, availability, specs)
- **Generic Extraction** - Falls back for any web page type

### Advanced Features
- **Rate Limiting** - Polite scraping with configurable delays
- **Caching** - Reduces redundant requests
- **robots.txt Compliance** - Respects website crawling policies
- **Batch Scraping** - Concurrent scraping of multiple URLs
- **Interactive Scraping** - Browser automation (clicks, forms, scrolling)
- **Infinite Scroll Support** - Handles dynamic content loading

## Installation

### Prerequisites

1. **Python 3.10+** - Required for the MCP server
2. **UV** - Fast Python package installer
3. **Playwright Browsers** - For browser-based scraping

### Setup

1. Navigate to the plugin directory:
```bash
cd plugin/web-scraper-plugin/mcp-server
```

2. Install Python dependencies:
```bash
uv pip install -r requirements.txt
```

3. Install Playwright browsers:
```bash
uv run playwright install chromium
```

4. The plugin is now ready to use with Claude Code!

## Available Tools

### `scrape_url`
Scrape a website and return its content.

**Parameters:**
- `url` (required) - The URL to scrape
- `use_browser` (optional) - Force browser mode
- `extract_content` (optional) - Extract main content only

**Example:**
```
Please scrape https://example.com and summarize the content
```

### `scrape_article`
Scrape an article or blog post.

**Parameters:**
- `url` (required) - The article URL

**Returns:**
- Title, author, date, content, tags, images

**Example:**
```
Extract the article from https://news.example.com/article-123
```

### `scrape_product`
Scrape an e-commerce product page.

**Parameters:**
- `url` (required) - The product URL

**Returns:**
- Product name, price, availability, description, images, specifications

**Example:**
```
Get product details from https://shop.example.com/item/456
```

### `extract_links`
Extract all links from a webpage.

**Parameters:**
- `url` (required) - URL to extract links from
- `filter_external` (optional) - Only return internal links

**Example:**
```
List all internal links on https://example.com
```

### `scrape_multiple`
Scrape multiple URLs concurrently.

**Parameters:**
- `urls` (required) - List of URLs to scrape
- `concurrent` (optional) - Max concurrent requests (default: 3)

**Example:**
```
Scrape these 5 URLs: https://site1.com, https://site2.com, https://site3.com
```

### `interactive_scrape`
Interact with a page using browser automation.

**Parameters:**
- `url` (required) - Starting URL
- `actions` (required) - List of actions to perform

**Action Types:**
- `{"type": "click", "selector": "css-selector"}`
- `{"type": "fill", "selector": "css-selector", "value": "text"}`
- `{"type": "wait", "ms": 1000}`
- `{"type": "scroll", "pixels": 500}`
- `{"type": "screenshot"}`

**Example:**
```
Go to https://example.com, fill in the search box with "test", click search, and scrape results
```

### `clear_cache`
Clear the scraping cache.

### `get_cache_stats`
Get cache statistics.

## Usage Examples

### Research Assistant
```
Scrape the documentation from https://docs.example.com and summarize the API endpoints
```

### Competitive Analysis
```
Extract pricing data from https://competitor.com/products and compare with our prices
```

### Content Migration
```
Scrape all articles from https://oldblog.example.com and convert them to markdown files
```

### Test Data Generation
```
Scrape product data from https://shop.example.com and create test JSON fixtures
```

## Architecture

```
web-scraper-plugin/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── mcp-server/
│   ├── server.py            # Main MCP server with tools
│   ├── scrapers/
│   │   ├── simple.py        # HTTP scraper (requests + BS4)
│   │   ├── browser.py       # Browser scraper (Playwright)
│   │   └── adaptive.py      # Smart router
│   ├── extractors/
│   │   ├── article.py       # Article content extraction
│   │   ├── product.py       # Product data extraction
│   │   └── generic.py       # Generic page extraction
│   ├── utils/
│   │   ├── cache.py         # Response caching
│   │   ├── rate_limiter.py  # Rate limiting
│   │   └── robots.py        # robots.txt parser
│   └── requirements.txt
├── .mcp.json                # MCP server configuration
└── README.md
```

## Configuration

### Rate Limiting
Adjust the default rate limit in `server.py`:
```python
rate_limiter = RateLimiter(requests_per_second=2.0)
```

### Cache TTL
Adjust cache duration:
```python
cache = CacheManager(ttl=3600)  # 1 hour
```

## Troubleshooting

### Playwright Browser Not Found
```bash
cd mcp-server
uv run playwright install chromium
```

### Import Errors
Make sure dependencies are installed:
```bash
cd mcp-server
uv pip install -r requirements.txt
```

### Permission Denied
Add to your `.claude/settings.local.json`:
```json
{
  "permissions": {
    "allow": ["Bash(*)", "Bash(cd:*)"]
  }
}
```

## Best Practices

1. **Be Respectful** - The plugin respects robots.txt and rate limits by default
2. **Use Cache** - Enable caching to avoid redundant requests
3. **Start Simple** - Try HTTP mode first, only use browser when needed
4. **Check robots.txt** - Some sites prohibit automated scraping
5. **Handle Errors** - Network failures and blocked requests are common

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please read CONTRIBUTING.md for guidelines.
