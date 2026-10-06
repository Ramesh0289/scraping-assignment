REQUIRED_FIELDS = [
    "source",
    "source_url",
    "name_or_title",
]


def validate_record(record):
    """
    Validate one normalized record.

    Returns:
        (True, None) when valid
        (False, reason) when invalid
    """

    # Check required fields
    for field in REQUIRED_FIELDS:
        value = record.get(field)

        if value is None or str(value).strip() == "":
            return False, f"missing_{field}"

    # Validate URL
    source_url = record.get("source_url")

    if not (
        str(source_url).startswith("http://")
        or str(source_url).startswith("https://")
    ):
        return False, "invalid_url"

    # Validate price
    price = record.get("price")

    if price is not None:
        try:
            price = float(price)

            if price < 0:
                return False, "negative_price"

        except (TypeError, ValueError):
            return False, "invalid_price"

    # Validate rating
    rating = record.get("rating")

    if rating is not None:
        try:
            rating = int(rating)

            if rating < 1 or rating > 5:
                return False, "invalid_rating"

        except (TypeError, ValueError):
            return False, "invalid_rating"

    return True, None