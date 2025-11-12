import sqlite3

DB_NAME = "employees.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            birth_date DATE NOT NULL,
            gender TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
