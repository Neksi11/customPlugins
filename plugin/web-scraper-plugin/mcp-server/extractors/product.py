"""
E-commerce product page extractor.

Extracts product information including name, price, availability,
description, images, and reviews from product pages.
"""

import re
from typing import Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup


class ProductExtractor:
    """Extract product information from e-commerce pages."""

    def __init__(self):
        # Common CSS selectors for product information
        self.price_selectors = [
            '[itemprop="price"]',
            '.price',
            '.product-price',
            '.current-price',
            '.sale-price',
            '.prize',
            '#priceblock_ourprice',
            '#priceblock_dealprice',
            '.a-price-whole'
        ]

        self.name_selectors = [
            '[itemprop="name"]',
            '.product-title',
            '.product-name',
            '.product-name-text',
            'h1.product-name',
            '#productTitle',
            '.title'
        ]

        self.availability_selectors = [
            '[itemprop="availability"]',
            '.stock',
            '.availability',
            '.product-availability',
            '#availability',
            '.in-stock',
            '.out-of-stock'
        ]

    def extract(self, html: str, url: str) -> dict:
        """
        Extract product information from HTML.

        Args:
            html: Raw HTML content
            url: Source URL

        Returns:
            Dict with product data
        """
        soup = BeautifulSoup(html, 'lxml')

        return {
            'name': self._extract_name(soup),
            'price': self._extract_price(soup),
            'availability': self._extract_availability(soup),
            'description': self._extract_description(soup),
            'images': self._extract_images(soup, url),
            'rating': self._extract_rating(soup),
            'reviews_count': self._extract_reviews_count(soup),
            'specifications': self._extract_specifications(soup),
            'variants': self._extract_variants(soup),
            'breadcrumbs': self._extract_breadcrumbs(soup),
            'metadata': self._extract_structured_data(soup)
        }

    def _extract_name(self, soup: BeautifulSoup) -> str:
        """Extract product name."""
        for selector in self.name_selectors:
            elem = soup.select_one(selector)
            if elem:
                # Try to get from itemprop content attribute first
                if elem.get('content'):
                    return elem.get('content')
                return elem.get_text(strip=True)

        # Try h1 as fallback
        h1 = soup.find('h1')
        if h1:
            return h1.get_text(strip=True)

        # Try og:title
        og_title = soup.find('meta', property='og:title')
        if og_title:
            return og_title.get('content', '')

        return ''

    def _extract_price(self, soup: BeautifulSoup) -> dict:
        """Extract product price information."""
        price_info = {
            'current': '',
            'original': '',
            'currency': '',
            'symbol': ''
        }

        # Try structured data first
        price_elem = soup.find('meta', itemprop='price')
        if price_elem:
            price_info['current'] = price_elem.get('content', '')

        currency_elem = soup.find('meta', itemprop='priceCurrency')
        if currency_elem:
            price_info['currency'] = currency_elem.get('content', '')

        # Try CSS selectors
        if not price_info['current']:
            for selector in self.price_selectors:
                elem = soup.select_one(selector)
                if elem:
                    price_info['current'] = (
                        elem.get('content', '') or
                        elem.get_text(strip=True)
                    )
                    break

        # Look for original/comparison price
        original_price = (
            soup.select_one('.original-price, .was-price, .list-price, .compare-price') or
            soup.find('meta', itemprop='price', attrs={'content': re.compile(r'\d')})
        )
        if original_price:
            price_info['original'] = (
                original_price.get('content', '') or
                original_price.get_text(strip=True)
            )

        # Extract currency symbol
        if price_info['current']:
            match = re.search(r'[\$\£\€\¥\₹]', price_info['current'])
            if match:
                price_info['symbol'] = match.group()

        return price_info

    def _extract_availability(self, soup: BeautifulSoup) -> dict:
        """Extract product availability information."""
        availability = {
            'status': '',
            'message': '',
            'in_stock': False
        }

        for selector in self.availability_selectors:
            elem = soup.select_one(selector)
            if elem:
                text = (
                    elem.get('content', '') or
                    elem.get_text(strip=True)
                ).lower()

                availability['message'] = text

                # Determine if in stock
                stock_keywords = ['in stock', 'available', 'add to cart', 'buy now']
                out_of_stock_keywords = ['out of stock', 'unavailable', 'sold out']

                if any(kw in text for kw in stock_keywords):
                    availability['status'] = 'in_stock'
                    availability['in_stock'] = True
                elif any(kw in text for kw in out_of_stock_keywords):
                    availability['status'] = 'out_of_stock'
                    availability['in_stock'] = False

                break

        return availability

    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract product description."""
        # Try structured data
        desc_elem = (
            soup.find('meta', itemprop='description') or
            soup.find('meta', attrs={'name': 'description'}) or
            soup.find(id='productDescription') or
            soup.find(class_=re.compile(r'description|details', re.I))
        )

        if desc_elem:
            text = (
                desc_elem.get('content', '') or
                desc_elem.get_text(strip=True)
            )
            return text[:5000]  # Limit length

        return ''

    def _extract_images(self, soup, url: str) -> list:
        """Extract product images."""
        images = []

        # Try structured data
        for img in soup.find_all('meta', property='og:image'):
            images.append({
                'url': img.get('content', ''),
                'type': 'primary'
            })

        # Try img tags
        for img in soup.find_all('img', src=True):
            src = img['src']
            # Resolve relative URLs
            if not src.startswith('http'):
                src = urljoin(url, src)

            # Filter likely product images by size keywords
            alt = img.get('alt', '').lower()
            class_str = ' '.join(img.get('class', [])).lower()

            if any(kw in alt + class_str for kw in ['product', 'item', 'main', 'zoom']):
                images.append({
                    'url': src,
                    'alt': img.get('alt', '')
                })

        return images[:10]

    def _extract_rating(self, soup: BeautifulSoup) -> dict:
        """Extract product rating."""
        rating = {'value': '', 'max': '5', 'count': ''}

        # Try structured data
        rating_elem = (
            soup.find('meta', itemprop='ratingValue') or
            soup.find(itemprop='ratingValue')
        )
        if rating_elem:
            rating['value'] = (
                rating_elem.get('content', '') or
                rating_elem.get_text(strip=True)
            )

        # Try CSS
        if not rating['value']:
            rating_elem = soup.select_one('.rating, .stars, .review-score')
            if rating_elem:
                text = rating_elem.get_text(strip=True)
                match = re.search(r'(\d+\.?\d*)', text)
                if match:
                    rating['value'] = match.group(1)

        return rating

    def _extract_reviews_count(self, soup: BeautifulSoup) -> str:
        """Extract number of reviews."""
        review_elem = (
            soup.find('meta', itemprop='reviewCount') or
            soup.select_one('[itemprop="reviewCount"]') or
            soup.find(class_=re.compile(r'review.*count', re.I))
        )

        if review_elem:
            text = (
                review_elem.get('content', '') or
                review_elem.get_text(strip=True)
            )
            match = re.search(r'(\d+)', text)
            if match:
                return match.group(1)

        return ''

    def _extract_specifications(self, soup: BeautifulSoup) -> list:
        """Extract product specifications."""
        specs = []

        # Look for specification tables
        tables = soup.find_all('table', class_=re.compile(r'spec|detail|tech', re.I))
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    specs.append({
                        'name': cells[0].get_text(strip=True),
                        'value': cells[1].get_text(strip=True)
                    })

        # Try structured data
        for spec in soup.find_all(itemprop='additionalProperty'):
            name = spec.find(itemprop='name')
            value = spec.find(itemprop='value')
            if name and value:
                specs.append({
                    'name': name.get_text(strip=True),
                    'value': value.get_text(strip=True)
                })

        return specs[:20]

    def _extract_variants(self, soup: BeautifulSoup) -> list:
        """Extract product variants (size, color, etc.)."""
        variants = []

        # Look for variant options
        for variant_type in ['color', 'size', 'style', 'material']:
            elem = soup.find(class_=re.compile(variant_type, re.I))
            if elem:
                options = elem.find_all(['option', 'button', 'a'], class_=re.compile(r'swatch|option|variant', re.I))
                variants.append({
                    'type': variant_type,
                    'options': [opt.get_text(strip=True) for opt in options if opt.get_text(strip=True)]
                })

        return variants

    def _extract_breadcrumbs(self, soup: BeautifulSoup) -> list:
        """Extract breadcrumb navigation."""
        breadcrumbs = []

        breadcrumb_elem = (
            soup.find('nav', {'aria-label': re.compile(r'breadcrumb', re.I)}) or
            soup.find(class_=re.compile(r'breadcrumb', re.I))
        )

        if breadcrumb_elem:
            for item in breadcrumb_elem.find_all('a', itemprop='item'):
                breadcrumbs.append({
                    'name': item.get_text(strip=True),
                    'url': item.get('href', '')
                })

        return breadcrumbs

    def _extract_structured_data(self, soup: BeautifulSoup) -> dict:
        """Extract JSON-LD structured data."""
        data = {}

        for script in soup.find_all('script', type='application/ld+json'):
            try:
                import json
                json_data = json.loads(script.string)
                if isinstance(json_data, dict):
                    data.update(json_data)
                elif isinstance(json_data, list) and json_data:
                    data.update(json_data[0])
            except:
                pass

        return data
