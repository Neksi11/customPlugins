"""
Rate limiter for polite scraping.

Prevents overwhelming servers with too many requests.
"""

import logging
import time
from typing import Dict
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Rate limiter using token bucket algorithm.

    Enforces delays between requests to the same domain.
    """

    def __init__(self, requests_per_second: float = 2.0, burst: int = 5):
        """
        Initialize rate limiter.

        Args:
            requests_per_second: Maximum sustained request rate
            burst: Maximum burst size (requests allowed instantly)
        """
        self.min_interval = 1.0 / requests_per_second
        self.burst = burst
        self._last_request: Dict[str, float] = {}
        self._request_count: Dict[str, int] = {}

    def _get_domain(self, url: str) -> str:
        """Extract domain from URL."""
        try:
            return urlparse(url).netloc or 'default'
        except:
            return 'default'

    def wait(self, url: str) -> None:
        """
        Wait if necessary to respect rate limits.

        Args:
            url: URL being requested
        """
        domain = self._get_domain(url)
        current_time = time.time()

        # Get last request time for this domain
        last_request = self._last_request.get(domain, 0)

        # Calculate time since last request
        time_since_last = current_time - last_request

        # Check if we need to wait
        if time_since_last < self.min_interval:
            wait_time = self.min_interval - time_since_last
            logger.debug(f"Rate limiting: waiting {wait_time:.2f}s for {domain}")
            time.sleep(wait_time)

        # Update last request time
        self._last_request[domain] = time.time()

        # Increment request count for burst tracking
        self._request_count[domain] = self._request_count.get(domain, 0) + 1

        # Reset burst counter if enough time has passed
        if time_since_last > self.burst * self.min_interval:
            self._request_count[domain] = 1

        # Check burst limit
        if self._request_count[domain] > self.burst:
            burst_wait = (self._request_count[domain] - self.burst) * self.min_interval
            logger.debug(f"Burst limit exceeded: waiting {burst_wait:.2f}s")
            time.sleep(burst_wait)

    def reset(self, domain: str = None) -> None:
        """
        Reset rate limiting for a domain or all domains.

        Args:
            domain: Specific domain to reset, or None for all
        """
        if domain:
            self._last_request.pop(domain, None)
            self._request_count.pop(domain, None)
        else:
            self._last_request.clear()
            self._request_count.clear()

    def get_stats(self) -> dict:
        """Get rate limiter statistics."""
        return {
            'domains_tracked': len(self._last_request),
            'min_interval': self.min_interval,
            'burst': self.burst,
            'requests_by_domain': self._request_count.copy()
        }

    def set_rate(self, requests_per_second: float) -> None:
        """
        Update the rate limit.

        Args:
            requests_per_second: New maximum request rate
        """
        self.min_interval = 1.0 / requests_per_second
        logger.info(f"Rate limit updated to {requests_per_second} requests/second")
