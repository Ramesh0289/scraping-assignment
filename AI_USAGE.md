# AI Usage Disclosure

## Overview

AI assistance was used during the development of this web scraping and data consolidation project.

The AI was used as a development aid, while the final implementation was reviewed, tested, and executed locally.

## Areas Where AI Was Used

### 1. Project Structure

AI assistance was used to understand the assignment requirements and organize the project into separate components:

- `scrapers/`
- `processing/`
- `tests/`
- `output/`
- `logs/`

### 2. Scraper Development

AI assistance helped with the initial implementation approach for:

- Requests session handling.
- HTTP timeouts.
- Retry configuration.
- User-Agent configuration.
- BeautifulSoup parsing.
- Dynamic pagination using the `Next` link.
- Mapping data from different websites into a common schema.

### 3. Data Cleaning

AI assistance was used to develop and review functions for:

- Whitespace normalization.
- Price conversion.
- Rating conversion.
- Tag normalization.
- URL normalization.
- Text cleanup.

### 4. Validation

AI assistance helped structure validation rules for:

- Required fields.
- URLs.
- Prices.
- Ratings.
- Invalid record handling.

### 5. Deduplication

AI assistance helped implement normalized fingerprints for identifying duplicate records.

The implemented approach is:

- Books: source + title.
- Quotes: source + author + first 50 characters of quote.

### 6. Testing

AI assistance was used to create initial unit test cases for:

- Cleaning.
- Validation.
- Deduplication.

The tests were executed locally using pytest and reviewed based on their actual results.

### 7. Debugging

AI assistance was used to diagnose development issues such as:

- Python package import errors.
- Missing `__init__.py` files.
- Test discovery issues.
- Data extraction and cleaning problems.

The fixes were tested locally before being retained.

### 8. Documentation

AI assistance was used to help draft and organize this README and AI usage disclosure.

## Human Review and Verification

The generated implementation was not accepted blindly.

The project was:

1. Reviewed manually.
2. Executed locally.
3. Tested using pytest.
4. Checked using generated CSV and JSON outputs.
5. Reviewed using execution logs.
6. Modified when data-quality issues were discovered.

For example, while reviewing the generated dataset, repeated text was identified in some book descriptions. The scraper was subsequently updated and rerun to improve the output.

## Final Validation

The project successfully completed the scraping pipeline and produced:

- `output/final_dataset.csv`
- `output/summary_report.json`
- `logs/scraper.log`

The current unit test suite contains 10 tests, all of which pass successfully.

## AI Limitations

AI-generated suggestions may contain implementation mistakes or assumptions. Therefore, all code used in the project was tested against the actual assignment requirements and local execution environment.

The final responsibility for the implementation and submitted project remains with the developer.