"""Web scraper implementations."""

from .simple import SimpleScraper
from .browser import BrowserScraper
from .adaptive import AdaptiveScraper

__all__ = ['SimpleScraper', 'BrowserScraper', 'AdaptiveScraper']
