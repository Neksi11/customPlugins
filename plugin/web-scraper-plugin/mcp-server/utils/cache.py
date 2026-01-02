"""
Simple in-memory cache for scraped content.

Reduces redundant requests and improves performance.
"""

import hashlib
import json
import logging
import time
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class CacheManager:
    """In-memory cache for scraped content."""

    def __init__(self, ttl: int = 3600, max_size: int = 1000):
        """
        Initialize cache.

        Args:
            ttl: Time to live for cache entries in seconds (default: 1 hour)
            max_size: Maximum number of entries to store
        """
        self.ttl = ttl
        self.max_size = max_size
        self._cache: Dict[str, Dict[str, Any]] = {}

    def _generate_key(self, url: str) -> str:
        """Generate cache key from URL."""
        return hashlib.md5(url.encode()).hexdigest()

    def get(self, url: str) -> Optional[dict]:
        """
        Get cached response for URL.

        Args:
            url: URL to lookup

        Returns:
            Cached response dict or None if not found/expired
        """
        key = self._generate_key(url)

        if key not in self._cache:
            return None

        entry = self._cache[key]

        # Check if expired
        if time.time() - entry['timestamp'] > self.ttl:
            del self._cache[key]
            logger.debug(f"Cache expired for {url}")
            return None

        logger.debug(f"Cache hit for {url}")
        return entry['data']

    def set(self, url: str, data: dict) -> None:
        """
        Cache response for URL.

        Args:
            url: URL being cached
            data: Response data to cache
        """
        key = self._generate_key(url)

        # Evict oldest entry if cache is full
        if len(self._cache) >= self.max_size:
            oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k]['timestamp'])
            del self._cache[oldest_key]
            logger.debug("Cache full, evicted oldest entry")

        self._cache[key] = {
            'data': data,
            'timestamp': time.time()
        }
        logger.debug(f"Cached response for {url}")

    def clear(self) -> None:
        """Clear all cached entries."""
        self._cache.clear()
        logger.info("Cache cleared")

    def get_stats(self) -> dict:
        """Get cache statistics."""
        return {
            'size': len(self._cache),
            'max_size': self.max_size,
            'ttl': self.ttl,
            'keys': list(self._cache.keys())
        }

    def remove(self, url: str) -> bool:
        """
        Remove specific URL from cache.

        Args:
            url: URL to remove

        Returns:
            True if removed, False if not found
        """
        key = self._generate_key(url)
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    def cleanup_expired(self) -> int:
        """Remove all expired entries. Returns number of entries removed."""
        current_time = time.time()
        expired_keys = [
            key for key, entry in self._cache.items()
            if current_time - entry['timestamp'] > self.ttl
        ]

        for key in expired_keys:
            del self._cache[key]

        logger.info(f"Cleaned up {len(expired_keys)} expired cache entries")
        return len(expired_keys)
