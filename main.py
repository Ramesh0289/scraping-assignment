import csv
import json
import logging
import os
import time
from datetime import datetime, timezone

from scrapers.books_scraper import BooksScraper
from scrapers.quotes_scraper import QuotesScraper

from processing.cleaning import (
    clean_text,
    strip_quotes,
    clean_price,
    clean_rating,
    clean_tags,
    normalize_url,
)

from processing.validation import validate_record
from processing.deduplication import remove_duplicates


OUTPUT_DIR = "output"
LOG_DIR = "logs"

CSV_FILE = os.path.join(
    OUTPUT_DIR,
    "final_dataset.csv"
)

JSON_FILE = os.path.join(
    OUTPUT_DIR,
    "summary_report.json"
)

LOG_FILE = os.path.join(
    LOG_DIR,
    "scraper.log"
)


def setup_logging():
    """Configure logging to both console and file."""

    os.makedirs(LOG_DIR, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(
                LOG_FILE,
                encoding="utf-8"
            ),
            logging.StreamHandler(),
        ],
    )


def clean_record(record):
    """Clean one scraped record."""

    return {
        "source": clean_text(record.get("source")),
        "source_url": normalize_url(
            record.get("source_url")
        ),
        "name_or_title": strip_quotes(
            record.get("name_or_title")
        ),
        "category": clean_text(
            record.get("category")
        ),
        "price": clean_price(
            record.get("price")
        ),
        "rating": clean_rating(
            record.get("rating")
        ),
        "author": clean_text(
            record.get("author")
        ),
        "tags": clean_tags(
            record.get("tags")
        ),
        "description": clean_text(
            record.get("description")
        ),
    }


def save_csv(records):
    """Save final records to CSV."""

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    fields = [
        "source",
        "source_url",
        "name_or_title",
        "category",
        "price",
        "rating",
        "author",
        "tags",
        "description",
        "scraped_at",
    ]

    with open(
        CSV_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fields
        )

        writer.writeheader()
        writer.writerows(records)


def main():
    """Run the complete scraping pipeline."""

    setup_logging()

    logger = logging.getLogger(__name__)

    start_time = time.time()
    start_timestamp = datetime.now(
        timezone.utc
    ).isoformat()

    logger.info("=" * 60)
    logger.info("SCRAPING ASSIGNMENT STARTED")
    logger.info("=" * 60)

    raw_records = []
    raw_counts = {
        "Books to Scrape": 0,
        "Quotes to Scrape": 0,
    }

    # ---------------------------------------------------------
    # 1. Scrape Books
    # ---------------------------------------------------------

    try:
        logger.info("Starting Books scraper...")

        books_scraper = BooksScraper()
        books_records = books_scraper.scrape()

        raw_records.extend(books_records)

        raw_counts["Books to Scrape"] = len(
            books_records
        )

        logger.info(
            "Books raw records: %d",
            len(books_records)
        )

    except Exception as exc:
        logger.exception(
            "Books scraper failed: %s",
            exc
        )

    # ---------------------------------------------------------
    # 2. Scrape Quotes
    # ---------------------------------------------------------

    try:
        logger.info("Starting Quotes scraper...")

        quotes_scraper = QuotesScraper()
        quotes_records = quotes_scraper.scrape()

        raw_records.extend(quotes_records)

        raw_counts["Quotes to Scrape"] = len(
            quotes_records
        )

        logger.info(
            "Quotes raw records: %d",
            len(quotes_records)
        )

    except Exception as exc:
        logger.exception(
            "Quotes scraper failed: %s",
            exc
        )

    # ---------------------------------------------------------
    # 3. Clean records
    # ---------------------------------------------------------

    cleaned_records = []

    for record in raw_records:
        cleaned_record = clean_record(record)
        cleaned_records.append(cleaned_record)

    logger.info(
        "Cleaned records: %d",
        len(cleaned_records)
    )

    # ---------------------------------------------------------
    # 4. Validate records
    # ---------------------------------------------------------

    valid_records = []
    rejected_count = 0
    rejection_reasons = {}

    for record in cleaned_records:

        is_valid, reason = validate_record(record)

        if is_valid:
            valid_records.append(record)

        else:
            rejected_count += 1

            rejection_reasons[reason] = (
                rejection_reasons.get(reason, 0) + 1
            )

    logger.info(
        "Valid records: %d",
        len(valid_records)
    )

    logger.info(
        "Rejected records: %d",
        rejected_count
    )

    # ---------------------------------------------------------
    # 5. Remove duplicates
    # ---------------------------------------------------------

    unique_records, duplicate_count = (
        remove_duplicates(valid_records)
    )

    logger.info(
        "Duplicates removed: %d",
        duplicate_count
    )

    # ---------------------------------------------------------
    # 6. Add scraped timestamp
    # ---------------------------------------------------------

    scraped_at = datetime.now(
        timezone.utc
    ).isoformat()

    for record in unique_records:
        record["scraped_at"] = scraped_at

    # ---------------------------------------------------------
    # 7. Save CSV
    # ---------------------------------------------------------

    save_csv(unique_records)

    logger.info(
        "Final dataset saved to %s",
        CSV_FILE
    )

    # ---------------------------------------------------------
    # 8. Create summary report
    # ---------------------------------------------------------

    end_time = time.time()
    end_timestamp = datetime.now(
        timezone.utc
    ).isoformat()

    summary = {
        "raw_counts": raw_counts,
        "cleaned_count": len(cleaned_records),
        "valid_count": len(valid_records),
        "rejected_count": rejected_count,
        "rejection_reasons": rejection_reasons,
        "duplicate_count": duplicate_count,
        "final_count": len(unique_records),
        "execution_duration_seconds": round(
            end_time - start_time,
            2
        ),
        "start_time": start_timestamp,
        "end_time": end_timestamp,
    }

    with open(
        JSON_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            summary,
            file,
            indent=4
        )

    logger.info(
        "Summary report saved to %s",
        JSON_FILE
    )

    logger.info("=" * 60)
    logger.info("SCRAPING ASSIGNMENT COMPLETED")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()