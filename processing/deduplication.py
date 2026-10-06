def normalize_for_fingerprint(value):
    """Normalize text before creating a fingerprint."""

    if value is None:
        return ""

    return " ".join(str(value).lower().split())


def create_fingerprint(record):
    """
    Create a unique fingerprint for a record.

    Books:
        source + title

    Quotes:
        source + author + first 50 characters of quote
    """

    source = normalize_for_fingerprint(
        record.get("source")
    )

    title = normalize_for_fingerprint(
        record.get("name_or_title")
    )

    author = normalize_for_fingerprint(
        record.get("author")
    )

    if source == "books to scrape":
        return f"{source}|{title}"

    if source == "quotes to scrape":
        quote_part = title[:50]

        return f"{source}|{author}|{quote_part}"

    return f"{source}|{title}|{author}"


def remove_duplicates(records):
    """Remove duplicate records and return unique records plus count."""

    seen = set()
    unique_records = []
    duplicate_count = 0

    for record in records:
        fingerprint = create_fingerprint(record)

        if fingerprint in seen:
            duplicate_count += 1
            continue

        seen.add(fingerprint)
        unique_records.append(record)

    return unique_records, duplicate_count