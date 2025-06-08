import json
import csv 
from pathlib import Path

class ReportStats:
    def __init__(self):
        self.file_reports = []
        
    def add_file_report(self, filename, valid, invalid, inserted):
        self.file_reports.append({
            "filename": filename,
            "valid": valid,
            "invalid": invalid,
            "inserted": inserted
        })
    
    def print_summary(self):
        print("\n--- FastCSV Report Summary ---")
        total_valid = sum(f["valid"] for f in self.file_reports)
        total_invalid = sum(f["invalid"] for f in self.file_reports)
        total_inserted = sum(f["inserted"] for f in self.file_reports)
        total_files = len(self.file_reports)
        
        print(f"Files processed: {total_files}")
        print(f"Valid rows: {total_valid}")
        print(f"Invalid rows: {total_invalid}")
        print(f"Inserted rows: {total_inserted}")
        
    def write_summary_json(self, path: Path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.file_reports, f, indent=2)
    
def export_invalid_rows(invalid_rows_by_file, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
        
    for filename, rows in invalid_rows_by_file.items():
        out_file = out_dir / f"{Path(filename).stem}_invalid.csv"
        if not rows:
            continue
        with open(out_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["row_number", "row_data", "errors"])
            for row_num, row, errors in rows:
                writer.writerow([row_num, row, "; ".join(errors)])