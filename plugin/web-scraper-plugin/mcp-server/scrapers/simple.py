"""
Simple HTTP scraper using requests + BeautifulSoup.

Fast and efficient for static websites, but cannot handle
JavaScript-rendered content.
"""

import asyncio
import logging
from typing import Optional

import aiohttp
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class SimpleScraper:
    """Fast HTTP-based scraper for static content."""

    def __init__(self, cache: Optional['CacheManager'] = None, rate_limiter: Optional['RateLimiter'] = None):
        self.cache = cache
        self.rate_limiter = rate_limiter
        self.session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=30)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            self.session = aiohttp.ClientSession(timeout=timeout, headers=headers)
        return self.session

    async def scrape(self, url: str, extract_content: bool = True) -> dict:
        """
        Scrape a URL using HTTP requests.

        Args:
            url: URL to scrape
            extract_content: Whether to extract main content only

        Returns:
            Dict with url, title, html, content, links
        """
        # Check cache first
        if self.cache:
            cached = self.cache.get(url)
            if cached:
                logger.info(f"Cache hit for {url}")
                return cached

        try:
            session = await self._get_session()

            async with session.get(url) as response:
                response.raise_for_status()
                html = await response.text()

            soup = BeautifulSoup(html, 'lxml')

            result = {
                'url': url,
                'title': soup.title.string if soup.title else '',
                'html': html,
                'status': 'success',
                'method': 'http'
            }

            if extract_content:
                result['content'] = self._extract_main_content(soup)
                result['text'] = soup.get_text(separator='\n', strip=True)

            result['links'] = self._extract_links(soup, url)

            # Cache the result
            if self.cache:
                self.cache.set(url, result)

            return result

        except aiohttp.ClientError as e:
            logger.error(f"HTTP error scraping {url}: {e}")
            return {
                'url': url,
                'error': str(e),
                'status': 'error',
                'method': 'http'
            }
        except Exception as e:
            logger.error(f"Unexpected error scraping {url}: {e}")
            return {
                'url': url,
                'error': str(e),
                'status': 'error',
                'method': 'http'
            }

    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """Extract the main content, removing navigation, footer, etc."""
        # Remove unwanted elements
        for tag in soup.find_all(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            tag.decompose()

        # Remove elements with common ad/class names
        for class_name in ['ad', 'advertisement', 'sidebar', 'menu', 'navigation', 'cookie']:
            for elem in soup.find_all(class_=lambda c: c and any(name in str(c).lower() for name in [class_name])):
                elem.decompose()

        # Try to find main content area
        main_content = (
            soup.find('main') or
            soup.find('article') or
            soup.find(class_=lambda c: c and any(name in str(c).lower() for name in ['content', 'main', 'article', 'post'])) or
            soup.body
        )

        if main_content:
            return main_content.get_text(separator='\n', strip=True)

        return soup.get_text(separator='\n', strip=True)

    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> list:
        """Extract all links from the page."""
        from urllib.parse import urljoin, urlparse

        links = []
        base_domain = urlparse(base_url).netloc

        for a in soup.find_all('a', href=True):
            href = a['href']
            text = a.get_text(strip=True)

            # Resolve relative URLs
            full_url = urljoin(base_url, href)
            link_domain = urlparse(full_url).netloc

            links.append({
                'text': text[:100],  # Limit text length
                'url': full_url,
                'internal': link_domain == base_domain
            })

        return links[:100]  # Limit to 100 links

    async def close(self):
        """Close the aiohttp session."""
        if self.session and not self.session.closed:
            await self.session.close()
