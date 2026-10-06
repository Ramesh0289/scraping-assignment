from processing.validation import validate_record


def test_valid_record():
    record = {
        "source": "Books to Scrape",
        "source_url": "https://books.toscrape.com/",
        "name_or_title": "Test Book",
        "price": 10.5,
        "rating": 4,
    }

    is_valid, reason = validate_record(record)

    assert is_valid is True
    assert reason is None


def test_missing_title():
    record = {
        "source": "Books to Scrape",
        "source_url": "https://books.toscrape.com/",
        "name_or_title": None,
        "price": 10.5,
        "rating": 4,
    }

    is_valid, reason = validate_record(record)

    assert is_valid is False
    assert reason == "missing_name_or_title"


def test_invalid_rating():
    record = {
        "source": "Books to Scrape",
        "source_url": "https://books.toscrape.com/",
        "name_or_title": "Test Book",
        "price": 10.5,
        "rating": 6,
    }

    is_valid, reason = validate_record(record)

    assert is_valid is False
    assert reason == "invalid_rating"