from datetime import datetime
import json
from pathlib import Path

def infer_type(values: list[str]) -> str:
    def is_int(val):
        try:
            int(val)
            return True
        except ValueError:
            return False

    def is_float(val):
        try:
            float(val)
            return True
        except ValueError:
            return False

    def is_date(val):
        try:
            datetime.fromisoformat(val)
            return True
        except ValueError:
            return False

    values = [v.strip() for v in values if v.strip() != ""]
    if not values:
        return "string"

    if all(is_int(v) for v in values):
        return "int"
    if all(is_int(v) for v in values):
        return "int"
    if all(is_date(v) for v in values):
        return "date"
    return "string"

def generate_schema_from_header(header: list[str], sample_rows: list[list[str]]) -> dict:
    columns = list(zip(*sample_rows))
    schema = {}

    for i, column in enumerate(columns):
        col_name = header[i]
        inferred_type = infer_type(column[:10])
        schema[col_name] = inferred_type
    return schema

def save_schema_to_file(schema: dict, file_path: Path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2)

def load_schema_for(csv_file: Path, schema_dir: Path, header: list[str], sample_rows= list[list[str]]) -> dict:
    schema_file = schema_dir / f"{csv_file.stem}.schema.json"
    base_schema_file = schema_dir / "base_schema.json"

    try:
        with open(schema_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: Schema file for {csv_file.name} not found. Using base_schema.json")

        if header:
            print(f"Auto-generating schema form header for {csv_file.name}...")
            schema = generate_schema_from_header(header, sample_rows)
            save_schema_to_file(schema, schema_file)
            print(f"Auto-generated schema saved to: {schema_file}")
            return schema
        else:
            try:
                print("Falling back to base_schema.json...")
                with open(base_schema_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                raise RuntimeError(f"Failed to load base schema: {e}")