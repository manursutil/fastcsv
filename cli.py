import argparse
import sys

def parse_args():
    parser = argparse.ArgumentParser(description="FastCSV: Universal CSV Validator")
    
    parser.add_argument("--dir", required=True, type=str, help="Path to the directory containing CSV files")
    parser.add_argument("--schema-dir", required=True, type=str, help="Path to the directory containing schema JSON files")
    parser.add_argument("--dry-run", action="store_true", help="Print CSV rows without processing")
    parser.add_argument("--log", action="store_true", help="Enable logging to file")
    parser.add_argument("--log-file", default="errors.log", help="Path to log file")
    parser.add_argument("--verbose", action="store_true", help="Print each row validation result")
    parser.add_argument("--limit", type=int, default=None, help="Limit rows per processed file")
    parser.add_argument("--db", choices=["sqlite", "postgres"], default="sqlite", help="Choose DB backend")
    parser.add_argument("--db-path", required="--dry-run" not in sys.argv, help="DB file path")
    parser.add_argument("--report-path", help="Save summary report to this file (.json)")
    parser.add_argument("--export-invalid", help="Directory to save invalid rows as .csv files")
    
    return parser.parse_args()