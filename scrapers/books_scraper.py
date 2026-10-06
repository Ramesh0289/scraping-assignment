from urllib.parse import urljoin

from bs4 import BeautifulSoup

from scrapers.base_scraper import BaseScraper


class BooksScraper(BaseScraper):
    """Scraper for Books to Scrape."""

    START_URL = "https://books.toscrape.com/"

    def parse_page(self, html, page_url):
        """Parse all books from one page."""

        soup = BeautifulSoup(html, "lxml")
        records = []

        books = soup.select("article.product_pod")

        for book in books:
            try:
                title_element = book.select_one("h3 > a")
                price_element = book.select_one("p.price_color")
                rating_element = book.select_one("p.star-rating")
                link_element = book.select_one("h3 > a")

                title = (
                    title_element.get("title")
                    if title_element
                    else None
                )

                price = (
                    price_element.get_text(strip=True)
                    if price_element
                    else None
                )

                rating = (
                    " ".join(rating_element.get("class", []))
                    if rating_element
                    else None
                )

                book_url = (
                    urljoin(
                        page_url,
                        link_element.get("href")
                    )
                    if link_element
                    and link_element.get("href")
                    else None
                )

                # Default values
                category = None
                description = None

                # Get additional information from
                # the individual book page
                if book_url:
                    detail_response = self.fetch_page(book_url)

                    if detail_response:
                        detail_soup = BeautifulSoup(
                            detail_response.text,
                            "lxml"
                        )

                        # -----------------------------
                        # Category
                        # -----------------------------

                        breadcrumb_links = detail_soup.select(
                            "ul.breadcrumb li a"
                        )

                        if breadcrumb_links:
                            category = breadcrumb_links[-1].get_text(
                                strip=True
                            )

                        # -----------------------------
                        # Description
                        # -----------------------------

                        description_element = detail_soup.select_one(
                            "#product_description + p"
                        )

                        if description_element:
                            description = (
                                description_element.get_text(
                                    " ",
                                    strip=True
                                )
                            )

                            # Remove repeated beginning
                            # found on some book pages.
                            if len(description) > 250:
                                prefix_length = 120

                                prefix = description[
                                    :prefix_length
                                ]

                                second_occurrence = (
                                    description.find(
                                        prefix,
                                        prefix_length
                                    )
                                )

                                if second_occurrence != -1:
                                    description = description[
                                        second_occurrence:
                                    ]

                records.append({
                    "source": "Books to Scrape",
                    "source_url": book_url,
                    "name_or_title": title,
                    "category": category,
                    "price": price,
                    "rating": rating,
                    "author": None,
                    "tags": None,
                    "description": description,
                })

            except Exception as exc:
                self.logger.warning(
                    "Could not parse a book on %s: %s",
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
                "Books page %d: %s",
                page_number,
                url
            )

            response = self.fetch_page(url)

            if response is None:
                self.logger.error(
                    "Stopping Books scraper at page %d",
                    page_number
                )
                break

            records = self.parse_page(
                response.text,
                url
            )

            all_records.extend(records)

            # Find the next page dynamically
            soup = BeautifulSoup(
                response.text,
                "lxml"
            )

            next_link = soup.select_one(
                "li.next > a"
            )

            if next_link and next_link.get("href"):
                url = urljoin(
                    url,
                    next_link["href"]
                )

                page_number += 1

            else:
                url = None

        self.logger.info(
            "Books scraper completed. Records collected: %d",
            len(all_records)
        )

        return all_records