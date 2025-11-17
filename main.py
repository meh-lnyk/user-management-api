from datetime import datetime
import random
import string
import sys
import time

from db import *
from employee import Employee, random_name, random_birth_date


# noinspection SpellCheckingInspection
def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <mode>")
        return

    mode = sys.argv[1]

    if mode == "1":
        print("Creating employees table...")
        create_table()
        print("Table created successfully")
    elif mode == "2":
        if len(sys.argv) != 5:
            print('Usage: python main.py 2 "Full Name" YYYY-MM-DD Gender')
            return

        _, _, full_name, birth_date, gender = sys.argv
        employee = Employee(full_name, birth_date, gender)
        employee.save_to_db()
        print(f"Employee saved: {employee.full_name}, age {employee.calculate_age()}")
    elif mode == "3":
        rows = fetch_all_employees()
        if not rows:
            print("No employees found.")
        else:
            for full_name, birth_date, gender in rows:
                emp = Employee(full_name, birth_date, gender)
                print(f"{emp.full_name}, {emp.birth_date}, {emp.gender}, {emp.calculate_age()} years")
    elif mode == "4":
        total = 1_000_000
        batch_size = 10_000
        extra_F_employees = 100

        print(f"Generating {total} employees...")
        employees = []
        genders = ["Male", "Female"]
        letters = list(string.ascii_uppercase)

        for i in range(total):
            gender = random.choice(genders)
            start_letter = letters[i % len(letters)]
            full_name = random_name(start_letter)
            birth_date = random_birth_date()
            employees.append(Employee(full_name, birth_date, gender))

            if len(employees) == batch_size:
                Employee.bulk_insert(employees)
                employees = []
                print(f"Inserted {i + 1}/{total}")

        print(f"Adding {extra_F_employees} extra Male employees with last name starting with 'F'...")
        extra_emps = [Employee(random_name("F"), random_birth_date(), "Male") for _ in range(extra_F_employees)]
        Employee.bulk_insert(extra_emps)
        print("Done!")
    elif mode == "5":
        print("Looking for male employees starting with 'F'...")
        start = time.perf_counter()
        rows = fetch_employees_by_criteria("F", "Male")
        if not rows:
            print("No employees found.")
        else:
            for full_name, birth_date, gender in rows:
                emp = Employee(full_name, birth_date, gender)
                print(f"{emp.full_name}, {emp.birth_date}, {emp.gender}")
            print("Done!")
        performance_time = time.perf_counter() - start
        print("Performance time: ", performance_time)

        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-log.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"=== Query Performance Log ===\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write(f"Query executed in: {performance_time:.6f} seconds\n")
            f.write(f"Rows found: {len(rows)}\n")
            f.write(f"Criteria: Male employees, full_name starting with 'F'\n\n")
        print(f"Log saved: {filename}")
    else:
        print("Unknown mode")

if __name__ == "__main__":
    main()
