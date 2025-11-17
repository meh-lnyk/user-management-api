import os
from datetime import datetime
import random
import string
import sys
import time

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
            f.write(f"Criteria: Male employees, full_name starting with 'F'\n")
        print(f"Log saved: {filename}")

        ru_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-log-ru.txt")
        with open(ru_filename, "w", encoding="utf-8") as f:
            f.write(f"=== Журнал производительности запроса ===\n")
            f.write(f"Дата: {datetime.now()}\n")
            f.write(f"Время выполнения запроса: {performance_time:.6f} секунд\n")
            f.write(f"Найдено строк: {len(rows)}\n")
            f.write(f"Критерии: Мужчины, full_name начинается с 'F'\n")
        print(f"RU log saved: {ru_filename}")
    elif mode == "6":
        LOG_DIR = "logs"
        os.makedirs(LOG_DIR, exist_ok=True)

        filename = os.path.join(
            LOG_DIR,
            datetime.now().strftime("%Y-%m-%d_%H-%M-%S-log.txt")
        )

        ru_filename = os.path.join(
            LOG_DIR,
            datetime.now().strftime("%Y-%m-%d_%H-%M-%S-log-ru.txt")
        )

        conn = sqlite3.connect("employees.db")
        cursor = conn.cursor()
        # Removing previous index if exists(in case it was left by the previous run of the script)
        cursor.execute("DROP INDEX IF EXISTS idx_fullname_gender")
        conn.commit()

        # Before optimization
        start1 = time.perf_counter()
        rows_before = fetch_employees_by_criteria("F", "Male")
        time_before = time.perf_counter() - start1

        # Creating index
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_fullname_gender
            ON employees(full_name, gender)
        """)
        conn.commit()
        conn.close()

        # After optimization
        start2 = time.perf_counter()
        rows_after = fetch_employees_by_criteria("F", "Male")
        time_after = time.perf_counter() - start2

        with open(filename, "w", encoding="utf-8") as f:
            f.write("=== Optimization Log ===\n")
            f.write(f"Date: {datetime.now()}\n\n")

            f.write("Before optimization:\n")
            f.write(f"Time: {time_before:.6f} seconds\n")
            f.write(f"Rows: {len(rows_before)}\n\n")

            f.write("Optimization:\n")
            f.write("Created index idx_fullname_gender\n")
            f.write("This index speeds up LIKE 'F%' + gender='Male'\n")
            f.write("by avoiding full table scan.\n\n")

            f.write("After optimization:\n")
            f.write(f"Time: {time_after:.6f} seconds\n")
            f.write(f"Rows: {len(rows_after)}\n")

        print(f"Optimization complete! Log saved: {filename}")

        with open(ru_filename, "w", encoding="utf-8") as f:
            f.write("=== Журнал оптимизации ===\n")
            f.write(f"Дата: {datetime.now()}\n\n")

            f.write("До оптимизации:\n")
            f.write(f"Время: {time_before:.6f} секунд\n")
            f.write(f"Строк найдено: {len(rows_before)}\n\n")

            f.write("Оптимизация:\n")
            f.write("Создан индекс idx_fullname_gender\n")
            f.write("Этот индекс ускоряет LIKE 'F%' + gender='Male'\n")
            f.write("за счёт избегания полного сканирования таблицы.\n\n")

            f.write("После оптимизации:\n")
            f.write(f"Время: {time_after:.6f} секунд\n")
            f.write(f"Строк найдено: {len(rows_after)}\n")

        print(f"Оптимизация завершена! Журнал сохранён: {ru_filename}")

    else:
        print("Unknown mode")

if __name__ == "__main__":
    main()
