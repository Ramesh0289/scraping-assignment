import re
from urllib.parse import urljoin


RATING_MAP = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
}


def clean_text(value):
    """Remove unnecessary whitespace and normalize text."""

    if value is None:
        return None

    value = value.replace("\xa0", " ")
    value = " ".join(value.split())

    return value if value else None


def strip_quotes(value):
    """Remove curly quotation marks from quote text."""

    if value is None:
        return None

    value = clean_text(value)

    if value and value.startswith("“"):
        value = value[1:]

    if value and value.endswith("”"):
        value = value[:-1]

    return value


def clean_price(value):
    """Convert a price such as £51.77 into a float."""

    if not value:
        return None

    match = re.search(
        r"\d+(?:\.\d+)?",
        value.replace(",", "")
    )

    if match:
        return float(match.group())

    return None


def clean_rating(value):
    """Convert a rating word such as Three into an integer."""

    if not value:
        return None

    for word in value.lower().split():
        if word in RATING_MAP:
            return RATING_MAP[word]

    return None


def clean_tags(tags):
    """Normalize tags and return them as a semicolon-separated string."""

    if not tags:
        return None

    cleaned_tags = []

    for tag in tags:
        cleaned = clean_text(tag)

        if cleaned:
            cleaned_tags.append(cleaned.lower())

    if not cleaned_tags:
        return None

    cleaned_tags = sorted(set(cleaned_tags))

    return ";".join(cleaned_tags)


def normalize_url(url, base_url=None):
    """Convert a URL into a complete HTTP/HTTPS URL."""

    if not url:
        return None

    url = url.strip()

    if base_url:
        url = urljoin(base_url, url)

    if url.startswith(("http://", "https://")):
        return url

    return None