import sys
from db import *
from employee import Employee

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
    else:
        print("Unknown mode")

if __name__ == "__main__":
    main()
