from pathlib import Path

def get_csv(directory):
    return list(Path(directory).rglob('*.csv'))