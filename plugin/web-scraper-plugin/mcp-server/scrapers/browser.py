"""
Browser-based scraper using Playwright.

Handles JavaScript-rendered content, dynamic pages, and allows
interaction with web pages.
"""

import asyncio
import base64
import logging
from typing import Optional, List

from playwright.async_api import async_playwright, Browser, Page, BrowserContext

logger = logging.getLogger(__name__)


class BrowserScraper:
    """Browser-based scraper for dynamic content."""

    def __init__(self, cache: Optional['CacheManager'] = None, headless: bool = True):
        self.cache = cache
        self.headless = headless
        self._playwright = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None

    async def _get_browser(self) -> Browser:
        """Get or create browser instance."""
        if self._browser is None or self._browser.is_connected():
            if self._playwright is None:
                self._playwright = await async_playwright().start()

            self._browser = await self._playwright.chromium.launch(
                headless=self.headless,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )

            # Create context with realistic viewport
            self._context = await self._browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )

        return self._browser

    async def _get_page(self) -> Page:
        """Get or create page."""
        await self._get_browser()
        if self._context:
            return await self._context.new_page()
        return await self._browser.new_page()

    async def scrape(self, url: str, wait_for: str = None, screenshot: bool = False) -> dict:
        """
        Scrape a URL using browser automation.

        Args:
            url: URL to scrape
            wait_for: CSS selector to wait for before scraping
            screenshot: Whether to capture screenshot

        Returns:
            Dict with url, title, html, content, screenshot (base64)
        """
        # Check cache first
        cache_key = f"browser:{url}"
        if self.cache and not screenshot:
            cached = self.cache.get(cache_key)
            if cached:
                logger.info(f"Cache hit for {url}")
                return cached

        page = None
        try:
            page = await self._get_page()

            # Navigate and wait for load
            await page.goto(url, wait_until='networkidle', timeout=30000)

            # Wait for specific element if requested
            if wait_for:
                await page.wait_for_selector(wait_for, timeout=10000)

            # Wait a bit for dynamic content
            await asyncio.sleep(1)

            # Extract content
            title = await page.title()
            html = await page.content()
            text = await page.evaluate('''() => {
                // Remove script/style content
                const clone = document.cloneNode(true);
                clone.querySelectorAll('script, style, nav, footer, header, aside').forEach(el => el.remove());
                return clone.body.innerText;
            }''')

            result = {
                'url': url,
                'title': title,
                'html': html,
                'text': text,
                'status': 'success',
                'method': 'browser'
            }

            # Capture screenshot if requested
            if screenshot:
                screenshot_bytes = await page.screenshot(full_page=False)
                result['screenshot'] = base64.b64encode(screenshot_bytes).decode()

            # Extract links
            result['links'] = await page.evaluate('''() => {
                return Array.from(document.querySelectorAll('a[href]')).slice(0, 100).map(a => ({
                    text: a.textContent.trim().slice(0, 100),
                    url: a.href,
                    internal: a.hostname === window.location.hostname
                }));
            }''')

            # Cache the result
            if self.cache and not screenshot:
                self.cache.set(cache_key, result)

            await page.close()
            return result

        except Exception as e:
            logger.error(f"Browser error scraping {url}: {e}")
            if page:
                try:
                    await page.close()
                except:
                    pass
            return {
                'url': url,
                'error': str(e),
                'status': 'error',
                'method': 'browser'
            }

    async def interactive_scrape(self, url: str, actions: List[dict]) -> dict:
        """
        Interact with a page before scraping.

        Actions:
        - {"type": "click", "selector": "css-selector"}
        - {"type": "fill", "selector": "css-selector", "value": "text"}
        - {"type": "wait", "ms": 1000}
        - {"type": "scroll", "pixels": 500}
        - {"type": "screenshot"}

        Args:
            url: Starting URL
            actions: List of actions to perform

        Returns:
            Dict with final page content
        """
        page = None
        try:
            page = await self._get_page()
            await page.goto(url, wait_until='networkidle', timeout=30000)

            for action in actions:
                action_type = action.get('type')

                if action_type == 'click':
                    await page.click(action['selector'], timeout=5000)
                    await asyncio.sleep(0.5)

                elif action_type == 'fill':
                    await page.fill(action['selector'], action['value'])
                    await asyncio.sleep(0.3)

                elif action_type == 'wait':
                    await asyncio.sleep(action.get('ms', 1000) / 1000)

                elif action_type == 'scroll':
                    await page.evaluate(f'window.scrollBy(0, {action.get("pixels", 500)})')
                    await asyncio.sleep(0.5)

                elif action_type == 'screenshot':
                    screenshot_bytes = await page.screenshot(full_page=False)
                    # Store for later

                elif action_type == 'wait_for_selector':
                    await page.wait_for_selector(action['selector'], timeout=10000)

                elif action_type == 'submit':
                    await page.press(action.get('selector', 'body'), 'Enter')
                    await asyncio.sleep(1)

            # Final scrape
            result = {
                'url': page.url,
                'title': await page.title(),
                'html': await page.content(),
                'text': await page.evaluate('''() => document.body.innerText'''),
                'status': 'success',
                'actions_performed': len(actions)
            }

            # Capture final screenshot
            screenshot_bytes = await page.screenshot(full_page=False)
            result['screenshot'] = base64.b64encode(screenshot_bytes).decode()

            await page.close()
            return result

        except Exception as e:
            logger.error(f"Interactive scrape error: {e}")
            if page:
                try:
                    await page.close()
                except:
                    pass
            return {
                'url': url,
                'error': str(e),
                'status': 'error'
            }

    async def scrape_infinite_scroll(self, url: str, max_scrolls: int = 5) -> dict:
        """
        Scrape a page with infinite scroll.

        Args:
            url: URL to scrape
            max_scrolls: Maximum number of scroll actions

        Returns:
            Dict with all loaded content
        """
        page = None
        try:
            page = await self._get_page()
            await page.goto(url, wait_until='networkidle')

            last_height = 0
            scrolls = 0

            while scrolls < max_scrolls:
                # Scroll to bottom
                await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                await asyncio.sleep(1)

                # Check if we've loaded new content
                new_height = await page.evaluate('document.body.scrollHeight')
                if new_height == last_height:
                    break
                last_height = new_height
                scrolls += 1

            result = {
                'url': url,
                'title': await page.title(),
                'html': await page.content(),
                'text': await page.evaluate('''() => document.body.innerText'''),
                'scrolls_completed': scrolls,
                'status': 'success'
            }

            await page.close()
            return result

        except Exception as e:
            logger.error(f"Infinite scroll error: {e}")
            if page:
                try:
                    await page.close()
                except:
                    pass
            return {
                'url': url,
                'error': str(e),
                'status': 'error'
            }

    async def close(self):
        """Close browser and cleanup resources."""
        if self._context:
            await self._context.close()
        if self._browser and self._browser.is_connected():
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
