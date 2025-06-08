import sqlite3
import psycopg2

def connect(db_type, db_path):
    if db_type == "sqlite":
        return sqlite3.connect(db_path)
    elif db_type == "postgres":
        return psycopg2.connect(db_path)
    else:
        raise ValueError("Unsupported DB type")

def create_table(conn, table_name, schema: dict):
    cols = []
    for col, typ in schema.items():
        sql_type = {
            "string": "TEXT",
            "int": "INTEGER",
            "float": "REAL",
            "date": "TEXT"
        }.get(typ, "TEXT")
        cols.append(f'"{col}" {sql_type}')
    col_str = ", ".join(cols)
    query = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({col_str});'
    conn.execute(query)
    conn.commit()

def insert_rows(conn, table_name, rows, schema):
    columns = list(schema.keys())
    placeholders = ", ".join(["?" for _ in columns])
    query = f'INSERT INTO "{table_name}" ({", ".join(columns)}) VALUES ({placeholders})'

    cur = conn.cursor()
    for row in rows:
        values = [row.get(col) for col in columns]
        cur.execute(query, values)
    conn.commit()