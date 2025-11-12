import sqlite3
from datetime import date, datetime


class Employee:
    def __init__(self, full_name: str, birth_date: str, gender: str):
        self.full_name = full_name
        self.birth_date = birth_date
        self.gender = gender

    def calculate_age(self) -> int:
        birth = datetime.strptime(self.birth_date, "%Y-%m-%d").date()
        today = date.today()
        return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))

    def save_to_db(self):
        conn = sqlite3.connect("employees.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO employees (full_name, birth_date, gender) VALUES (?, ?, ?)",
            (self.full_name, self.birth_date, self.gender)
        )
        conn.commit()
        conn.close()
