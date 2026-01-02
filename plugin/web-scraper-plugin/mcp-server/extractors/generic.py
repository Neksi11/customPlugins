"""
Generic content extractor for general web pages.

Provides fallback extraction when specialized extractors aren't applicable.
"""

import re
from typing import Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup


class GenericExtractor:
    """Generic content extraction for any web page."""

    def __init__(self):
        self.remove_selectors = [
            'script', 'style', 'noscript', 'iframe',
            'nav', 'footer', 'header', 'aside',
            '.navigation', '.menu', '.sidebar',
            '.cookie', '.popup', '.modal',
            '.advertisement', '.ad'
        ]

    def extract(self, html: str, url: str) -> dict:
        """
        Extract content from any web page.

        Args:
            html: Raw HTML content
            url: Source URL

        Returns:
            Dict with page content
        """
        soup = BeautifulSoup(html, 'lxml')

        return {
            'url': url,
            'title': self._extract_title(soup),
            'description': self._extract_description(soup),
            'content': self._extract_content(soup),
            'headings': self._extract_headings(soup),
            'links': self._extract_links(soup, url),
            'images': self._extract_images(soup, url),
            'metadata': self._extract_metadata(soup),
            'forms': self._extract_forms(soup),
            'tables': self._extract_tables(soup)
        }

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title."""
        # Try OpenGraph title
        og_title = soup.find('meta', property='og:title')
        if og_title:
            return og_title.get('content', '')

        # Try Twitter title
        twitter_title = soup.find('meta', attrs={'name': 'twitter:title'})
        if twitter_title:
            return twitter_title.get('content', '')

        # Try title tag
        if soup.title:
            return soup.title.get_text(strip=True)

        # Try h1
        h1 = soup.find('h1')
        if h1:
            return h1.get_text(strip=True)

        return ''

    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract page description."""
        desc_elem = (
            soup.find('meta', attrs={'name': 'description'}) or
            soup.find('meta', property='og:description') or
            soup.find('meta', attrs={'name': 'twitter:description'})
        )

        if desc_elem:
            return desc_elem.get('content', '')

        return ''

    def _extract_content(self, soup: BeautifulSoup) -> dict:
        """Extract main page content."""
        # Remove unwanted elements
        cleaned = soup.__copy__()

        for selector in self.remove_selectors:
            for elem in cleaned.select(selector):
                elem.decompose()

        # Extract text content
        text = cleaned.get_text(separator='\n', strip=True)

        # Try to find main content area
        main_content = (
            cleaned.find('main') or
            cleaned.find('article') or
            cleaned.find(id=re.compile(r'content|main', re.I)) or
            cleaned.find(class_=re.compile(r'content|main', re.I))
        )

        if main_content:
            main_text = main_content.get_text(separator='\n', strip=True)
        else:
            main_text = text

        # Extract paragraphs
        paragraphs = []
        for p in cleaned.find_all('p'):
            text = p.get_text(strip=True)
            if len(text) > 20:
                paragraphs.append(text)

        return {
            'full_text': text[:10000],  # Limit length
            'main_text': main_text[:5000],
            'paragraphs': paragraphs[:50]
        }

    def _extract_headings(self, soup: BeautifulSoup) -> dict:
        """Extract page headings structure."""
        headings = {'h1': [], 'h2': [], 'h3': [], 'h4': [], 'h5': [], 'h6': []}

        for level in range(1, 7):
            tag = f'h{level}'
            for heading in soup.find_all(tag):
                text = heading.get_text(strip=True)
                if text:
                    headings[tag].append({
                        'text': text,
                        'id': heading.get('id', '')
                    })

        return headings

    def _extract_links(self, soup, url: str) -> dict:
        """Extract all links from page."""
        from urllib.parse import urlparse

        base_domain = urlparse(url).netloc
        all_links = []
        internal_links = []
        external_links = []

        for a in soup.find_all('a', href=True):
            href = a['href']
            text = a.get_text(strip=True)
            title = a.get('title', '')

            # Skip empty links
            if not text or href in ['#', 'javascript:', 'javascript:void(0)']:
                continue

            # Resolve relative URLs
            if not href.startswith('http'):
                href = urljoin(url, href)

            link_data = {
                'text': text[:100],
                'url': href,
                'title': title
            }

            link_domain = urlparse(href).netloc
            if link_domain == base_domain:
                link_data['type'] = 'internal'
                internal_links.append(link_data)
            else:
                link_data['type'] = 'external'
                external_links.append(link_data)

            all_links.append(link_data)

        return {
            'all': all_links[:100],
            'internal': internal_links[:50],
            'external': external_links[:50]
        }

    def _extract_images(self, soup, url: str) -> list:
        """Extract all images from page."""
        images = []

        for img in soup.find_all('img', src=True):
            src = img['src']

            # Resolve relative URLs
            if not src.startswith('http'):
                src = urljoin(url, src)

            image_data = {
                'src': src,
                'alt': img.get('alt', ''),
                'title': img.get('title', ''),
                'width': img.get('width', ''),
                'height': img.get('height', '')
            }

            # Check if image has parent link
            if img.parent and img.parent.name == 'a':
                image_data['link'] = img.parent.get('href', '')

            images.append(image_data)

        return images[:50]

    def _extract_metadata(self, soup: BeautifulSoup) -> dict:
        """Extract page metadata."""
        metadata = {}

        # OpenGraph
        for meta in soup.find_all('meta', property=True):
            prop = meta.get('property')
            if prop.startswith('og:'):
                metadata[prop] = meta.get('content', '')

        # Twitter Card
        for meta in soup.find_all('meta', attrs={'name': True}):
            name = meta.get('name')
            if name.startswith('twitter:'):
                metadata[name] = meta.get('content', '')

        # Standard meta tags
        for meta in soup.find_all('meta', attrs={'name': True}):
            name = meta.get('name')
            if name in ['keywords', 'author', 'robots', 'viewport']:
                metadata[name] = meta.get('content', '')

        # Canonical URL
        canonical = soup.find('link', rel='canonical')
        if canonical:
            metadata['canonical_url'] = canonical.get('href', '')

        return metadata

    def _extract_forms(self, soup: BeautifulSoup) -> list:
        """Extract form information."""
        forms = []

        for form in soup.find_all('form'):
            form_data = {
                'action': form.get('action', ''),
                'method': form.get('method', 'GET').upper(),
                'fields': []
            }

            for input_elem in form.find_all(['input', 'select', 'textarea']):
                field = {
                    'type': input_elem.get('type', 'text'),
                    'name': input_elem.get('name', ''),
                    'id': input_elem.get('id', ''),
                    'required': input_elem.has_attr('required')
                }

                if field['name'] or field['id']:
                    form_data['fields'].append(field)

            forms.append(form_data)

        return forms

    def _extract_tables(self, soup: BeautifulSoup) -> list:
        """Extract table data."""
        tables = []

        for table in soup.find_all('table'):
            table_data = {'headers': [], 'rows': []}

            # Extract headers
            headers = table.find_all('th')
            if headers:
                table_data['headers'] = [th.get_text(strip=True) for th in headers]

            # Extract rows
            for tr in table.find_all('tr'):
                cells = [td.get_text(strip=True) for td in tr.find_all('td')]
                if cells:
                    table_data['rows'].append(cells)

            if table_data['headers'] or table_data['rows']:
                tables.append(table_data)

        return tables[:10]
