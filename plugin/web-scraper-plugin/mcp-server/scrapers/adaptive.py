"""
Adaptive scraper that intelligently chooses between HTTP and browser methods.

Analyzes the target URL and content to determine the optimal scraping strategy.
"""

import asyncio
import logging
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .simple import SimpleScraper
    from .browser import BrowserScraper
    from utils.robots import RobotsTxtParser

logger = logging.getLogger(__name__)


class AdaptiveScraper:
    """
    Intelligent scraper that routes between HTTP and browser methods.

    Strategy:
    1. Try simple HTTP first (fast, lightweight)
    2. Fall back to browser if:
       - HTTP returns empty/meaningless content
       - Page has known JavaScript framework indicators
       - Explicitly requested
    3. Respect robots.txt rules
    """

    # Patterns that indicate JavaScript-heavy sites
    JS_FRAMEWORK_INDICATORS = [
        'react', 'vue', 'angular', 'nextjs', 'nuxt',
        '__next', 'nuxt-root', 'ng-app', 'data-reactroot',
        '_gatsby', 'gatsby'
    ]

    # Domains known to require JavaScript
    JS_REQUIRED_DOMAINS = [
        'twitter.com', 'x.com', 'facebook.com', 'instagram.com',
        'linkedin.com', 'youtube.com', 'tiktok.com', 'reddit.com'
    ]

    def __init__(
        self,
        simple_scraper: 'SimpleScraper',
        browser_scraper: 'BrowserScraper',
        robots_parser: Optional['RobotsTxtParser'] = None
    ):
        self.simple_scraper = simple_scraper
        self.browser_scraper = browser_scraper
        self.robots_parser = robots_parser

    async def scrape(
        self,
        url: str,
        extract_content: bool = True,
        use_browser: bool = False,
        fallback_to_browser: bool = True
    ) -> dict:
        """
        Scrape a URL using the optimal method.

        Args:
            url: URL to scrape
            extract_content: Whether to extract main content
            use_browser: Force browser mode
            fallback_to_browser: Fall back to browser if HTTP fails

        Returns:
            Dict with scraped content
        """
        # Check robots.txt
        if self.robots_parser and not self.robots_parser.is_allowed(url):
            logger.warning(f"Robots.txt disallows scraping: {url}")
            return {
                'url': url,
                'error': 'Disallowed by robots.txt',
                'status': 'blocked'
            }

        # Force browser mode if requested
        if use_browser or self._should_use_browser(url):
            logger.info(f"Using browser for {url}")
            return await self.browser_scraper.scrape(url)

        # Try simple HTTP first
        logger.info(f"Trying HTTP scraper for {url}")
        result = await self.simple_scraper.scrape(url, extract_content=extract_content)

        # Fall back to browser if HTTP failed and fallback is enabled
        if fallback_to_browser and self._should_fallback(result):
            logger.info(f"HTTP failed for {url}, falling back to browser")
            browser_result = await self.browser_scraper.scrape(url)
            browser_result['fallback_from'] = 'http'
            return browser_result

        return result

    def _should_use_browser(self, url: str) -> bool:
        """Determine if browser should be used based on URL."""
        url_lower = url.lower()

        # Check for JavaScript-required domains
        for domain in self.JS_REQUIRED_DOMAINS:
            if domain in url_lower:
                return True

        return False

    def _should_fallback(self, result: dict) -> bool:
        """Determine if we should fall back to browser based on HTTP result."""
        # Don't fallback if there was an actual error
        if 'error' in result and result['error']:
            # But do fallback for certain errors
            error_lower = str(result['error']).lower()
            if any(e in error_lower for e in ['timeout', 'connection', 'redirect']):
                return True
            return False

        # Check if content is too short or empty
        html = result.get('html', '')
        if len(html) < 1000:
            return True

        # Check for JavaScript framework indicators
        html_lower = html.lower()
        for indicator in self.JS_FRAMEWORK_INDICATORS:
            if indicator in html_lower:
                # Also check if actual content is minimal
                if len(result.get('content', '')) < 500:
                    return True

        # Check for common "enable JavaScript" messages
        js_required_messages = [
            'enable javascript',
            'javascript must be enabled',
            'please enable javascript',
            'this site requires javascript'
        ]
        for msg in js_required_messages:
            if msg in html_lower:
                return True

        return False

    async def batch_scrape(
        self,
        urls: list[str],
        concurrent: int = 3,
        prefer_http: bool = True
    ) -> list[dict]:
        """
        Scrape multiple URLs concurrently.

        Args:
            urls: List of URLs to scrape
            concurrent: Maximum concurrent requests
            prefer_http: Try HTTP first for all URLs

        Returns:
            List of results in same order as URLs
        """
        semaphore = asyncio.Semaphore(concurrent)

        async def scrape_one(url: str) -> dict:
            async with semaphore:
                # For batch operations, prefer HTTP for speed
                result = await self.scrape(
                    url,
                    use_browser=not prefer_http,
                    fallback_to_browser=True
                )
                return result

        tasks = [scrape_one(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        formatted_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                formatted_results.append({
                    'url': urls[i],
                    'error': str(result),
                    'status': 'error'
                })
            else:
                formatted_results.append(result)

        return formatted_results
