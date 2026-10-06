# Multi-Source Web Scraping and Data Consolidation Pipeline

## 1. Project Overview

This project is a Python-based web scraping and data consolidation pipeline.

It collects data from two public websites:

- Books to Scrape — https://books.toscrape.com/
- Quotes to Scrape — https://quotes.toscrape.com/

The scraped data is cleaned, validated, deduplicated, and combined into a common dataset.

The final outputs are:

- `output/final_dataset.csv`
- `output/summary_report.json`
- `logs/scraper.log`

---

## 2. Features

- Scrapes all available pages dynamically using the website's **Next** link.
- Supports multiple independent data sources.
- Uses a shared HTTP scraping class.
- Includes request timeout and retry handling.
- Uses a custom User-Agent.
- Adds a delay between requests.
- Normalizes scraped data into a common schema.
- Cleans text, prices, ratings, tags, and URLs.
- Validates required fields and data types.
- Rejects invalid records without stopping the complete pipeline.
- Removes duplicate records using normalized fingerprints.
- Generates CSV and JSON output files.
- Maintains execution logs.
- Includes unit tests using pytest.

---

## 3. Project Architecture

The pipeline follows this flow:

```text
Web Sources
    |
    v
Scrapers
    |
    v
Raw Records
    |
    v
Cleaning
    |
    v
Validation
    |
    v
Deduplication
    |
    v
Final Dataset
    |
    +----> CSV
    |
    +----> Summary JSON
    |
    +----> Logs
```

---

## 4. Project Structure

```text
scraping_assignment/
│
├── scrapers/
│   ├── __init__.py
│   ├── base_scraper.py
│   ├── books_scraper.py
│   └── quotes_scraper.py
│
├── processing/
│   ├── __init__.py
│   ├── cleaning.py
│   ├── validation.py
│   └── deduplication.py
│
├── tests/
│   ├── __init__.py
│   ├── test_cleaning.py
│   ├── test_validation.py
│   └── test_deduplication.py
│
├── output/
│   ├── final_dataset.csv
│   └── summary_report.json
│
├── logs/
│   └── scraper.log
│
├── main.py
├── requirements.txt
├── README.md
├── AI_USAGE.md
├── .gitignore
└── sample_execution.txt
```

---

## 5. Technologies Used

- Python
- Requests
- BeautifulSoup
- lxml
- pytest
- CSV
- JSON
- Python logging

---

## 6. Installation

Create and activate a virtual environment:

```powershell
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

---

## 7. Running the Project

Run the complete pipeline:

```powershell
python main.py
```

The pipeline will:

1. Scrape Books to Scrape.
2. Scrape Quotes to Scrape.
3. Clean the collected records.
4. Validate the records.
5. Remove duplicates.
6. Add the scraping timestamp.
7. Save the final CSV.
8. Generate the summary JSON.
9. Write execution logs.

---

## 8. Data Sources

### Books to Scrape

Source:

https://books.toscrape.com/

The scraper collects:

- Book title
- Book URL
- Category
- Price
- Rating
- Description

The scraper follows the `Next` page link until no further page exists.

### Quotes to Scrape

Source:

https://quotes.toscrape.com/

The scraper collects:

- Quote text
- Quote page URL
- Author
- Tags

The scraper also follows the `Next` page link dynamically.

---

## 9. Common Data Schema

The final dataset contains:

| Field | Description |
|---|---|
| `source` | Website from which the record was collected |
| `source_url` | Source URL |
| `name_or_title` | Book title or quote text |
| `category` | Book category where available |
| `price` | Book price where available |
| `rating` | Rating from 1 to 5 where available |
| `author` | Quote author where available |
| `tags` | Quote tags where available |
| `description` | Book description where available |
| `scraped_at` | UTC timestamp when the record was processed |

Fields that are not applicable to a particular source are stored as empty values.

---

## 10. Data Cleaning

The cleaning layer performs:

- Whitespace normalization.
- Removal of unnecessary non-breaking spaces.
- Price conversion into numeric values.
- Rating conversion from words such as `Three` into integers such as `3`.
- Tag normalization.
- Duplicate tag removal.
- URL normalization.
- Quote text cleanup.

Example:

```text
"  Hello    World  "
```

becomes:

```text
"Hello World"
```

Example:

```text
"£51.77"
```

becomes:

```text
51.77
```

---

## 11. Validation

Each cleaned record is validated before being included in the final dataset.

Validation checks include:

- Required source field.
- Required source URL.
- Required title/name or quote text.
- Valid HTTP/HTTPS URL.
- Valid numeric price.
- Non-negative price.
- Rating between 1 and 5.

Invalid records are rejected with a reason and the pipeline continues processing.

---

## 12. Deduplication

Duplicate records are removed using normalized fingerprints.

### Books

The fingerprint is based on:

```text
source + book title
```

### Quotes

The fingerprint is based on:

```text
source + author + first 50 characters of quote
```

Text is normalized before creating the fingerprint so differences in case or whitespace do not create unnecessary duplicates.

---

## 13. Error Handling

The scraper includes:

- Request timeouts.
- HTTP retry handling.
- Handling for common temporary HTTP errors.
- Logging of failed requests.
- Handling of page parsing errors.
- Source-level exception handling.
- Continued processing when one source fails.

The Books and Quotes scrapers are executed independently so a failure in one source does not unnecessarily stop the other source.

---

## 14. Output Files

### `output/final_dataset.csv`

Contains the cleaned, validated, and deduplicated records.

### `output/summary_report.json`

Contains:

- Raw record counts by source.
- Cleaned record count.
- Valid record count.
- Rejected record count.
- Rejection reasons.
- Duplicate count.
- Final record count.
- Execution duration.
- Start timestamp.
- End timestamp.

### `logs/scraper.log`

Contains the execution history, including:

- Pages fetched.
- Scraper progress.
- Errors and warnings.
- Record counts.
- Output file creation.

---

## 15. Testing

Unit tests are implemented using pytest.

Run:

```powershell
pytest -v
```

The tests cover:

- Text cleaning.
- Price cleaning.
- Rating cleaning.
- Tag cleaning.
- URL normalization.
- Record validation.
- Missing required fields.
- Invalid ratings.
- Fingerprint creation.
- Duplicate removal.

Current test result:

```text
10 passed
```

---

## 16. Design Decisions

### Dynamic pagination

The project does not hard-code the number of pages. It follows the `Next` link until the website indicates there are no more pages.

### Shared HTTP layer

Common request functionality is placed in `BaseScraper` so both website scrapers can reuse:

- Requests session.
- User-Agent.
- Timeout.
- Retry configuration.
- Request delay.
- Error logging.

### Separate processing layer

Cleaning, validation, and deduplication are kept separate from scraping so each responsibility can be tested independently.

### Common schema

Both websites produce different types of information, so the project maps them into the same final schema. Fields that do not apply to a source remain empty.

---

## 17. Example Execution Result

A successful execution currently produces approximately:

```text
Books to Scrape: 1000
Quotes to Scrape: 100
Cleaned records: 1100
Valid records: 1100
Rejected records: 0
Duplicates removed: 1
Final records: 1099
```

The exact execution time and timestamps may vary between runs.

---

## 18. AI Assistance

AI assistance was used during development for:

- Understanding the assignment requirements.
- Structuring the project.
- Drafting initial implementation ideas.
- Debugging Python issues.
- Creating and reviewing unit tests.
- Improving documentation.

All generated code was reviewed, tested, and executed locally before inclusion in the project.

More details are provided in `AI_USAGE.md`.

---

## 19. Limitations

- The project depends on the HTML structure of the target websites.
- Website layout changes may require selector updates.
- Some fields are source-specific and therefore remain empty when they are not applicable.
- Internet connectivity is required to run the live scraping pipeline.

---

## 20. License

This project was created as an interview/assessment project for educational and evaluation purposes.