from pathlib import Path
from tqdm import tqdm

from cli import parse_args
from db.db import connect, create_table, insert_rows
from logger import setup_logger
from reader import read_csv_files
from schema.schema_loader import load_schema_for
from validator import validate_row
from report import ReportStats, export_invalid_rows

def main():
    args = parse_args()
    logger = setup_logger(args.log, args.log_file)

    schema_dir = Path(args.schema_dir)
    data_dir = Path(args.dir)
    all_files = read_csv_files(data_dir)
    
    conn = None
    if not args.dry_run:
        logger.info(f"Connecting to {args.db}...")
        conn = connect(args.db, args.db_path)

    report = ReportStats()
    invalid_rows_by_file = {}

    for filename, rows in all_files.items():
        csv_path = data_dir / filename
        header = rows[0]
        data_rows = rows[1:]
        schema = load_schema_for(csv_path, schema_dir, header, data_rows)

        valid_count = 0
        invalid_count = 0
        valid_rows = []
        invalid_rows = []

        logger.info(f"\nProcessing files: {filename}")
        for i, row in enumerate(tqdm(data_rows, desc=filename), start=2):
            row_dict = dict(zip(header, row))
            is_valid, errors = validate_row(row_dict, schema)

            if is_valid:
                valid_count += 1
                valid_rows.append(row_dict)
                if args.verbose:
                    logger.info(f"Row {i} OK")
            else:
                invalid_count += 1
                invalid_rows.append((i, row, errors))
                logger.warning(f"{filename} row {i} invalid: {errors}")

        logger.info(f"Finished {filename} → Valid: {valid_count}, Invalid: {invalid_count}")
        
        if not args.dry_run and valid_rows:
            table_name = filename.replace(".csv", "").strip().lower()
            create_table(conn, table_name, schema)
            insert_rows(conn, table_name, valid_rows, schema)
            logger.info(f"Inserted {len(valid_rows)} rows into table '{table_name}'")
            
        report.add_file_report(filename, len(valid_rows), len(invalid_rows), inserted=len(valid_rows))
        invalid_rows_by_file[filename] = invalid_rows
        
        report.print_summary()
        if args.report_path:
            report.write_summary_json(Path(args.report_path))
            
        if args.export_invalid:
            export_invalid_rows(invalid_rows_by_file, Path(args.export_invalid))
            
        if conn:
            conn.close()
            logger.info("Connections closed.")
            
if __name__ == "__main__":
    main()