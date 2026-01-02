"""
Article and blog post content extractor.

Optimized for news sites, blogs, documentation, and similar content.
"""

import re
from typing import Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup


class ArticleExtractor:
    """Extract article content from HTML."""

    def __init__(self):
        # Common CSS selectors for article content
        self.content_selectors = [
            'article',
            '[role="main"]',
            '.post-content',
            '.article-content',
            '.entry-content',
            '.content',
            '#content',
            '.post-body',
            '.article-body',
            'main',
        ]

        # CSS selectors to remove
        self.remove_selectors = [
            'nav', 'footer', 'header', 'aside',
            '.sidebar', '.menu', '.navigation',
            '.related-posts', '.comments',
            '.share-buttons', '.social-share',
            'script', 'style', 'noscript',
            '.ad', '.advertisement', '.sponsored',
            '.cookie-notice', '.popup', '.modal'
        ]

    def extract(self, html: str, url: str) -> dict:
        """
        Extract article content from HTML.

        Args:
            html: Raw HTML content
            url: Source URL (for resolving relative links)

        Returns:
            Dict with article data
        """
        soup = BeautifulSoup(html, 'lxml')

        # Find article content
        content_elem = self._find_content(soup)
        if not content_elem:
            content_elem = soup.find('body') or soup

        # Clean up the content
        cleaned_soup = self._clean_content(content_elem)

        # Extract metadata
        metadata = self._extract_metadata(soup, url)

        # Extract main content
        content = self._extract_text(cleaned_soup)

        # Extract images
        images = self._extract_images(cleaned_soup, url)

        # Extract links
        links = self._extract_links(cleaned_soup, url)

        return {
            'title': metadata.get('title', ''),
            'author': metadata.get('author', ''),
            'date': metadata.get('date', ''),
            'content': content,
            'excerpt': self._create_excerpt(content),
            'word_count': len(content.split()),
            'images': images[:10],  # Limit to 10 images
            'links': links[:20],   # Limit to 20 links
            'tags': metadata.get('tags', []),
            'metadata': metadata
        }

    def _find_content(self, soup: BeautifulSoup) -> Optional:
        """Find the main article content element."""
        for selector in self.content_selectors:
            elem = soup.select_one(selector)
            if elem:
                return elem
        return None

    def _clean_content(self, soup):
        """Remove unwanted elements from content."""
        # Create a copy to avoid modifying original
        cleaned = soup.__copy__()

        # Remove unwanted elements
        for selector in self.remove_selectors:
            for elem in cleaned.select(selector):
                elem.decompose()

        return cleaned

    def _extract_metadata(self, soup: BeautifulSoup, url: str) -> dict:
        """Extract article metadata."""
        metadata = {}

        # Title
        title_elem = (
            soup.find('meta', property='og:title') or
            soup.find('meta', attrs={'name': 'twitter:title'}) or
            soup.find('h1')
        )
        metadata['title'] = (
            title_elem.get('content', '') if hasattr(title_elem, 'get') else
            title_elem.get_text(strip=True) if title_elem else
            soup.title.get_text(strip=True) if soup.title else ''
        )

        # Author
        author_elem = (
            soup.find('meta', attrs={'name': 'author'}) or
            soup.find('meta', property='article:author') or
            soup.find(class_=lambda c: c and 'author' in str(c).lower())
        )
        metadata['author'] = (
            author_elem.get('content', '') if hasattr(author_elem, 'get') else
            author_elem.get_text(strip=True) if author_elem else ''
        )

        # Date
        date_elem = (
            soup.find('meta', property='article:published_time') or
            soup.find('meta', attrs={'name': 'date'}) or
            soup.find('meta', attrs={'name': 'publish_date'}) or
            soup.find(class_=lambda c: c and any(word in str(c).lower() for word in ['date', 'time', 'published']))
        )
        metadata['date'] = (
            date_elem.get('content', '') if hasattr(date_elem, 'get') else
            date_elem.get('datetime', '') if hasattr(date_elem, 'get') else
            date_elem.get_text(strip=True) if date_elem else ''
        )

        # Tags/keywords
        keywords_elem = soup.find('meta', attrs={'name': 'keywords'})
        tags = []
        if keywords_elem:
            tags = [t.strip() for t in keywords_elem.get('content', '').split(',')]

        # Also check for article:tag
        for tag_elem in soup.find_all('meta', property='article:tag'):
            tags.append(tag_elem.get('content', ''))

        metadata['tags'] = tags

        # Description
        desc_elem = (
            soup.find('meta', attrs={'name': 'description'}) or
            soup.find('meta', property='og:description')
        )
        metadata['description'] = desc_elem.get('content', '') if desc_elem else ''

        return metadata

    def _extract_text(self, soup) -> str:
        """Extract clean text content."""
        # Get all paragraphs
        paragraphs = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li'])

        texts = []
        for p in paragraphs:
            text = p.get_text(strip=True)
            if text and len(text) > 20:  # Filter out very short fragments
                texts.append(text)

        return '\n\n'.join(texts)

    def _create_excerpt(self, content: str, max_length: int = 300) -> str:
        """Create a short excerpt from content."""
        if len(content) <= max_length:
            return content

        # Try to break at sentence boundary
        excerpt = content[:max_length]
        last_period = excerpt.rfind('.')
        if last_period > max_length * 0.7:  # If period is in last 30%
            return excerpt[:last_period + 1]

        return excerpt + '...'

    def _extract_images(self, soup, url: str) -> list:
        """Extract images with captions."""
        images = []
        for img in soup.find_all('img', src=True):
            src = img['src']
            # Resolve relative URLs
            if not src.startswith('http'):
                src = urljoin(url, src)

            image_data = {'src': src}

            # Get alt text
            if img.get('alt'):
                image_data['alt'] = img['alt']

            # Look for caption/figcaption
            if img.parent and img.parent.name == 'figure':
                caption = img.parent.find('figcaption')
                if caption:
                    image_data['caption'] = caption.get_text(strip=True)

            images.append(image_data)

        return images

    def _extract_links(self, soup, url: str) -> list:
        """Extract relevant links from content."""
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            text = a.get_text(strip=True)

            # Resolve relative URLs
            if not href.startswith('http'):
                href = urljoin(url, href)

            if text and len(text) > 0:
                links.append({'text': text[:100], 'url': href})

        return links
