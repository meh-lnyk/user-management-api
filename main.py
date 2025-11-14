import random
import string
import sys
from db import *
from employee import Employee, random_name, random_birth_date


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
    else:
        print("Unknown mode")

if __name__ == "__main__":
    main()
