import sys
from db import create_table

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <mode>")
        return

    mode = sys.argv[1]

    if mode == "1":
        print("Creating employees table...")
        create_table()
        print("Table created successfully")
    else:
        print("Unknown mode")

if __name__ == "__main__":
    main()
