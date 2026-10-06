from processing.deduplication import (
    create_fingerprint,
    remove_duplicates,
)


def test_book_fingerprint():
    record = {
        "source": "Books to Scrape",
        "name_or_title": "Test Book",
    }

    fingerprint = create_fingerprint(record)

    assert fingerprint == "books to scrape|test book"


def test_remove_duplicate_books():
    records = [
        {
            "source": "Books to Scrape",
            "name_or_title": "Test Book",
        },
        {
            "source": "Books to Scrape",
            "name_or_title": "Test Book",
        },
    ]

    unique_records, duplicate_count = remove_duplicates(
        records
    )

    assert len(unique_records) == 1
    assert duplicate_count == 1