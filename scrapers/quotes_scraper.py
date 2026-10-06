from urllib.parse import urljoin

from bs4 import BeautifulSoup

from scrapers.base_scraper import BaseScraper


class QuotesScraper(BaseScraper):
    """Scraper for Quotes to Scrape."""

    START_URL = "https://quotes.toscrape.com/"

    def parse_page(self, html, page_url):
        """Parse all quotes from one page."""

        soup = BeautifulSoup(html, "lxml")
        records = []

        quotes = soup.select("div.quote")

        for quote in quotes:
            try:
                text_element = quote.select_one("span.text")
                author_element = quote.select_one("small.author")

                tag_elements = quote.select("a.tag")

                quote_text = (
                    text_element.get_text(strip=True)
                    if text_element
                    else None
                )

                author = (
                    author_element.get_text(strip=True)
                    if author_element
                    else None
                )

                tags = [
                    tag.get_text(strip=True)
                    for tag in tag_elements
                ]

                quote_url = page_url

                records.append({
                    "source": "Quotes to Scrape",
                    "source_url": quote_url,
                    "name_or_title": quote_text,
                    "category": None,
                    "price": None,
                    "rating": None,
                    "author": author,
                    "tags": tags,
                    "description": None,
                })

            except Exception as exc:
                self.logger.warning(
                    "Could not parse a quote on %s: %s",
                    page_url,
                    exc
                )

        return records

    def scrape(self):
        """Scrape all available pages by following the Next link."""

        url = self.START_URL
        all_records = []
        page_number = 1

        while url:

            self.logger.info(
                "Quotes page %d: %s",
                page_number,
                url
            )

            response = self.fetch_page(url)

            if response is None:
                self.logger.error(
                    "Stopping Quotes scraper at page %d",
                    page_number
                )
                break

            records = self.parse_page(
                response.text,
                url
            )

            all_records.extend(records)

            soup = BeautifulSoup(response.text, "lxml")

            next_link = soup.select_one("li.next > a")

            if next_link and next_link.get("href"):
                url = urljoin(
                    url,
                    next_link["href"]
                )
                page_number += 1
            else:
                url = None

        self.logger.info(
            "Quotes scraper completed. Records collected: %d",
            len(all_records)
        )

        return all_records