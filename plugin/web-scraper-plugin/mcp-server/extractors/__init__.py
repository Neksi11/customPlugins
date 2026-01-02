"""Content extractors for different page types."""

from .article import ArticleExtractor
from .product import ProductExtractor
from .generic import GenericExtractor

__all__ = ['ArticleExtractor', 'ProductExtractor', 'GenericExtractor']
