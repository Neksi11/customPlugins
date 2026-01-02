"""
Robots.txt parser for respecting website rules.

Ensures the scraper respects website crawling policies.
"""

import logging
import time
from typing import Dict, Optional, Set
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class RobotsTxtParser:
    """
    Simple robots.txt parser.

    Implements a subset of the robots.txt specification
    focused on common use cases.
    """

    def __init__(self, cache_ttl: int = 86400):
        """
        Initialize parser.

        Args:
            cache_ttl: Cache time for robots.txt in seconds (default: 24 hours)
        """
        self.cache_ttl = cache_ttl
        self._cache: Dict[str, Dict] = {}
        self._disallowed_cache: Dict[str, Set[str]] = {}

    def _get_robots_url(self, url: str) -> str:
        """Get robots.txt URL for given URL."""
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}/robots.txt"

    def _parse_robots_txt(self, content: str, user_agent: str = '*') -> dict:
        """
        Parse robots.txt content.

        Args:
            content: Raw robots.txt content
            user_agent: User agent to check (default: *)

        Returns:
            Dict with allow, disallow, crawl_delay rules
        """
        rules = {'allow': [], 'disallow': [], 'crawl_delay': 0}

        lines = content.split('\n')
        current_agent = None
        matching_group = False

        for line in lines:
            line = line.strip()

            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue

            # Parse key-value pairs
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()

                if key == 'user-agent':
                    # Check if this group matches our user agent
                    if value.lower() == user_agent.lower() or value == '*':
                        matching_group = True
                        current_agent = value
                    else:
                        matching_group = False

                elif matching_group:
                    if key == 'disallow':
                        if value:
                            rules['disallow'].append(value)
                    elif key == 'allow':
                        if value:
                            rules['allow'].append(value)
                    elif key == 'crawl-delay':
                        try:
                            rules['crawl_delay'] = float(value)
                        except ValueError:
                            pass

        return rules

    async def _fetch_robots_txt(self, url: str) -> Optional[str]:
        """Fetch robots.txt for URL."""
        import aiohttp

        robots_url = self._get_robots_url(url)

        try:
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(robots_url) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        # If robots.txt doesn't exist, allow everything
                        logger.debug(f"No robots.txt found for {robots_url}")
                        return None
        except Exception as e:
            logger.warning(f"Failed to fetch robots.txt for {robots_url}: {e}")
            # On error, allow everything (be permissive)
            return None

    def _path_matches_rule(self, path: str, rule: str) -> bool:
        """Check if a path matches a robots.txt rule."""
        if rule == '/':
            return True
        if rule == '':
            return False
        if path.startswith(rule):
            return True
        # Simple wildcard support
        if '*' in rule:
            pattern = rule.replace('*', '.*')
            import re
            if re.match(pattern, path):
                return True
        return False

    def is_allowed(self, url: str, user_agent: str = '*') -> bool:
        """
        Check if URL is allowed by robots.txt.

        Args:
            url: URL to check
            user_agent: User agent to check as

        Returns:
            True if allowed, False if disallowed
        """
        try:
            parsed = urlparse(url)
            path = parsed.path or '/'

            # Check if we have cached rules for this domain
            domain = parsed.netloc
            current_time = time.time()

            if domain in self._cache:
                cached = self._cache[domain]
                if current_time - cached['timestamp'] < self.cache_ttl:
                    rules = cached['rules']
                else:
                    # Cache expired, we'll allow (lazy refresh)
                    return True
            else:
                # No cache yet, allow (will be populated asynchronously)
                return True

            # Check disallow rules
            for rule in rules['disallow']:
                if self._path_matches_rule(path, rule):
                    # Check if there's a matching allow rule (more specific)
                    allowed = False
                    for allow_rule in rules['allow']:
                        if self._path_matches_rule(path, allow_rule):
                            if len(allow_rule) >= len(rule):
                                allowed = True
                                break
                    if not allowed:
                        logger.info(f"Disallowed by robots.txt: {url}")
                        return False

            return True

        except Exception as e:
            logger.error(f"Error checking robots.txt for {url}: {e}")
            return True  # Allow on error

    async def preload_rules(self, url: str) -> None:
        """
        Preload robots.txt rules for a domain.

        Args:
            url: URL to fetch robots.txt for
        """
        import asyncio

        parsed = urlparse(url)
        domain = parsed.netloc

        # Check if already cached and fresh
        if domain in self._cache:
            cached = self._cache[domain]
            if time.time() - cached['timestamp'] < self.cache_ttl:
                return

        # Fetch robots.txt
        content = await self._fetch_robots_txt(url)

        if content:
            rules = self._parse_robots_txt(content)
        else:
            # No robots.txt means allow everything
            rules = {'allow': [], 'disallow': [], 'crawl_delay': 0}

        self._cache[domain] = {
            'rules': rules,
            'timestamp': time.time()
        }

        logger.info(f"Loaded robots.txt rules for {domain}")

    def get_rules(self, url: str) -> dict:
        """Get cached robots.txt rules for a domain."""
        parsed = urlparse(url)
        domain = parsed.netloc

        if domain in self._cache:
            return self._cache[domain]['rules']

        return {'allow': [], 'disallow': [], 'crawl_delay': 0}

    def clear_cache(self) -> None:
        """Clear all cached robots.txt rules."""
        self._cache.clear()
        logger.info("Robots.txt cache cleared")
