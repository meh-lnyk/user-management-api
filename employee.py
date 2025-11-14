import random
import sqlite3
import string
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

    @staticmethod
    def bulk_insert(employees):
        conn = sqlite3.connect("employees.db")
        cursor = conn.cursor()
        cursor.executemany(
            "INSERT INTO employees (full_name, birth_date, gender) VALUES (?, ?, ?)",
            [(emp.full_name, emp.birth_date, emp.gender) for emp in employees]
        )
        conn.commit()
        conn.close()

def random_name(start_letter=None):
    letters = string.ascii_uppercase
    if start_letter:
        surname = start_letter + ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
    else:
        surname = random.choice(letters) + ''.join(random.choice(string.ascii_lowercase) for _ in range(5))

    # For code simplicity I won't add a check for female gender when assigning names
    # so only male names and patronymics are listed here
    name = random.choice(["Ivan", "Petr", "Sergei", "Alexander", "Mikhail"])
    patronymic = random.choice(["Ivanovich", "Petrovich", "Sergeevich", "Alexandrovich", "Mikhailovich"])

    return f"{surname} {name} {patronymic}"

def random_birth_date():
    year = random.randint(1950, 2005)
    month = random.randint(1, 12)
    if month == 2:
        day = random.randint(1, 28)
    elif month in (4, 6, 9, 11):
        day = random.randint(1, 30)
    else:
        day = random.randint(1, 31)
    return f"{year:04d}-{month:02d}-{day:02d}"
