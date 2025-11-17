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

def fetch_all_employees():
    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT full_name, birth_date, gender
        FROM employees
        GROUP BY full_name, birth_date
        ORDER BY full_name
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def fetch_employees_by_criteria(fullname: str, gender: str):
    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT full_name, birth_date, gender
        FROM employees
        WHERE full_name LIKE ?
            AND gender = ?
    """, (fullname + "%", gender))
    rows = cursor.fetchall()
    conn.close()
    return rows
