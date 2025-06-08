# FastCSV

** A fast, schema-aware CSV ingestion and validation pipeline built with Python**
FastCSV is a simple CLI tool that reads multiple '.csv' files, validates them against JSON-based schemas, and stores clean data into SQLite or ProstgreSQL databases.

---

## Features

- Automatic schema inference (with override support).
- Per-row validation with detailed error logging.
- Insert clean data into SQLite or PostgreSQL.
- Summary repporting of valid, invalid and inserted rows.
- Optional export of invalid rows.
- Fully command-line control.
- Modular codebase: easy to extend with your won validators or exporters.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/manursutil/fastcsv.git
cd fastcsv
```

(Optional) Create virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## CLI Flags

| Flag             | Description                                |
| ---------------- | ------------------------------------------ |
| --dir            | Directory containing CSV files             |
| --schema-dir     | Directory of JSON schemas                  |
| --db             | Databse type: sqlite or postgres           |
| --db-path        | Path to .db file                           |
| --dry-run        | Validate without inserting into db         |
| --report-path    | Save summary report as .json               |
| --export-invalid | Output directory for invalid rows (as CSV) |
| --log            | Enable loggin to file                      |
| --log-file       | Path to log file                           |
| --verbose        | Print each row validation result           |

## CLI Usage

Basic usage:

```bash
python main.py \
  --dir data \
  --schema-dir schema \
  --db sqlite \
  --db-path fastcsv.db \
  --report-path summary.json \
  --export-invalid invalid_rows \
  --log
```

---

## Example Output

```bash
Processing: customers.csv
Row 3 invalid: ['age: invalid literal for int() with base 10: "notanumber"']

Summary for customers.csv:
Total rows: 3
Valid rows: 2
Invalid rows: 1

=== FastCSV Report Summary ===
Files processed: 1
Valid rows: 2
Invalid rows: 1
Inserted rows: 2
```

---

## Schema Format

Schemas are defines as .json files and auto-matched by filename. Example:

```bash
{
  "name": "string",
  "age": "int",
  "email": "string",
  "signup_date": "date"
}
```

If no schema is found, FastCSV infers one from the first few rows.

---

## Tech Stack

- Python 3.12.4
- SQLite / PostgreSQL
- argparse, csv, json, tqdm

---

## License

This project is licensed under the MIT License.
See [`LICENSE`](./LICENSE) for details.

---

## Contributions

Contributions are welcome! If you'd like to extend FastCSV (e.g., support YAML schemas, add validation rules, or build a GUI), open an issue or fork the repo.
