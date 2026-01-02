#!/usr/bin/env python3
"""
Web Scraper MCP Server

An intelligent web scraping server with adaptive HTTP/browser fallback,
content extraction, and automation capabilities.
"""

import asyncio
import json
from typing import Any, Optional
from urllib.parse import urlparse

from fastmcp import FastMCP

from scrapers.adaptive import AdaptiveScraper
from scrapers.simple import SimpleScraper
from scrapers.browser import BrowserScraper
from extractors.article import ArticleExtractor
from extractors.product import ProductExtractor
from extractors.generic import GenericExtractor
from utils.cache import CacheManager
from utils.rate_limiter import RateLimiter
from utils.robots import RobotsTxtParser

# Initialize MCP server
mcp = FastMCP("web-scraper")

# Initialize components
cache = CacheManager()
rate_limiter = RateLimiter()
robots_parser = RobotsTxtParser()
simple_scraper = SimpleScraper(cache=cache, rate_limiter=rate_limiter)
browser_scraper = BrowserScraper(cache=cache)
adaptive_scraper = AdaptiveScraper(
    simple_scraper=simple_scraper,
    browser_scraper=browser_scraper,
    robots_parser=robots_parser
)
article_extractor = ArticleExtractor()
product_extractor = ProductExtractor()
generic_extractor = GenericExtractor()


@mcp.tool()
async def scrape_url(url: str, use_browser: bool = False, extract_content: bool = True) -> str:
    """
    Scrape a website and return its content.

    Args:
        url: The URL to scrape
        use_browser: Force browser mode (Playwright) instead of HTTP
        extract_content: Extract main content (removes nav, footer, ads)

    Returns:
        JSON string with scraped content including url, title, content, links
    """
    try:
        rate_limiter.wait(url)

        if use_browser:
            result = await browser_scraper.scrape(url)
        else:
            result = await adaptive_scraper.scrape(url, extract_content=extract_content)

        return json.dumps(result, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e), "url": url}, indent=2)


@mcp.tool()
async def scrape_article(url: str) -> str:
    """
    Scrape an article/blog post and extract the main content.

    Optimized for news sites, blogs, and documentation.

    Args:
        url: The article URL to scrape

    Returns:
        JSON with title, author, content, date, tags, images
    """
    try:
        rate_limiter.wait(url)
        html_content = await adaptive_scraper.scrape(url, extract_content=False)
        result = article_extractor.extract(html_content.get('html', ''), url)
        result['url'] = url
        return json.dumps(result, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e), "url": url}, indent=2)


@mcp.tool()
async def scrape_product(url: str) -> str:
    """
    Scrape an e-commerce product page.

    Extracts product name, price, availability, description, images, reviews.

    Args:
        url: The product page URL

    Returns:
        JSON with product details
    """
    try:
        rate_limiter.wait(url)
        html_content = await adaptive_scraper.scrape(url, extract_content=False, use_browser=True)
        result = product_extractor.extract(html_content.get('html', ''), url)
        result['url'] = url
        return json.dumps(result, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e), "url": url}, indent=2)


@mcp.tool()
async def extract_links(url: str, filter_external: bool = False) -> str:
    """
    Extract all links from a webpage.

    Args:
        url: The URL to extract links from
        filter_external: Only return links from the same domain

    Returns:
        JSON array of links with text and URL
    """
    try:
        rate_limiter.wait(url)
        result = await adaptive_scraper.scrape(url, extract_content=False)

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(result.get('html', ''), 'lxml')
        base_domain = urlparse(url).netloc

        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            text = a.get_text(strip=True)

            # Resolve relative URLs
            if href.startswith('/'):
                base = f"{urlparse(url).scheme}://{base_domain}"
                href = base + href
            elif not href.startswith('http'):
                continue

            # Filter external links if requested
            if filter_external:
                link_domain = urlparse(href).netloc
                if link_domain != base_domain:
                    continue

            links.append({"text": text, "url": href})

        return json.dumps({"url": url, "links": links}, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e), "url": url}, indent=2)


@mcp.tool()
async def scrape_multiple(urls: list[str], concurrent: int = 3) -> str:
    """
    Scrape multiple URLs concurrently.

    Args:
        urls: List of URLs to scrape
        concurrent: Maximum concurrent requests

    Returns:
        JSON array of results
    """
    results = []
    semaphore = asyncio.Semaphore(concurrent)

    async def scrape_one(url: str):
        async with semaphore:
            return json.loads(await scrape_url(url))

    tasks = [scrape_one(url) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    formatted_results = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            formatted_results.append({"url": urls[i], "error": str(result)})
        else:
            formatted_results.append(result)

    return json.dumps(formatted_results, indent=2, ensure_ascii=False)


@mcp.tool()
async def interactive_scrape(url: str, actions: list[dict]) -> str:
    """
    Interact with a page using browser automation.

    Actions format:
    - {"type": "click", "selector": "css-selector"}
    - {"type": "fill", "selector": "css-selector", "value": "text"}
    - {"type": "wait", "ms": 1000}
    - {"type": "scroll", "pixels": 500}
    - {"type": "screenshot"}

    Args:
        url: Starting URL
        actions: List of actions to perform

    Returns:
        JSON with final page content and optionally screenshot
    """
    try:
        result = await browser_scraper.interactive_scrape(url, actions)
        return json.dumps(result, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e), "url": url}, indent=2)


@mcp.tool()
async def search_and_scrape(query: str, num_results: int = 5) -> str:
    """
    Search the web and scrape the top results.

    Note: This performs scraping of discovered URLs. For actual search,
    consider integrating a search API.

    Args:
        query: Search query
        num_results: Number of results to scrape

    Returns:
        JSON with scraped content from top results
    """
    # This is a simplified version - in production, integrate with search APIs
    # like Google Custom Search, Bing Search API, or DuckDuckGo
    return json.dumps({
        "error": "Search API integration required",
        "message": "Integrate with search API (Google, Bing, DuckDuckGo) for full functionality"
    }, indent=2)


@mcp.tool()
def clear_cache() -> str:
    """Clear the scraping cache."""
    cache.clear()
    return json.dumps({"status": "success", "message": "Cache cleared"}, indent=2)


@mcp.tool()
def get_cache_stats() -> str:
    """Get cache statistics."""
    stats = cache.get_stats()
    return json.dumps(stats, indent=2)


if __name__ == "__main__":
    mcp.run()
