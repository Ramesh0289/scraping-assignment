import logging
import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


class BaseScraper:
    """Shared HTTP functionality for all website scrapers."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": "ScrapingAssignment/1.0 (learning project)"
        })

        retries = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )

        adapter = HTTPAdapter(max_retries=retries)

        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        self.timeout = 10
        self.delay = 0.5

    def fetch_page(self, url):
        """Fetch a webpage safely and return the response."""

        try:
            self.logger.info("Fetching page: %s", url)

            response = self.session.get(
                url,
                timeout=self.timeout
            )

            response.raise_for_status()

            response.encoding = "utf-8"

            time.sleep(self.delay)

            return response

        except requests.RequestException as exc:
            self.logger.error(
                "Failed to fetch %s: %s",
                url,
                exc
            )

            return None