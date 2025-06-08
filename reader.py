import csv
from pathlib import Path
from utils.path_utils import get_csv

def read_csv_files(directory):
    data = {}
    files = get_csv(directory)

    for file in files:
        try:
            with open(file, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
                data[file.name] = rows
        except Exception as e:
            print(f"Failed to read {file}: {e}")

    return data