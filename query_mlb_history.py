import sqlite3

# Connect to the database
conn = sqlite3.connect('mlb_history.db')
cursor = conn.cursor()

print("Welcome to MLB History Database Query Tool")

def main_menu():
    while True:
        print("\nWhat would you like to do?")
        print("1. Show all records")
        print("2. Filter by year")
        print("3. Filter by event keyword")
        print("4. Custom SQL query")
        print("5. Exit")

        choice = input("Enter choice (1-5): ")

        if choice == "1":
            show_all()
        elif choice == "2":
            filter_by_year()
        elif choice == "3":
            filter_by_event()
        elif choice == "4":
            custom_query()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Try again.")

def show_all():
    try:
        cursor.execute("SELECT * FROM mlb_history_1902")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except sqlite3.Error as e:
        print("Error:", e)

def filter_by_year():
    year = input("Enter year: ")
    try:
        cursor.execute("SELECT * FROM mlb_history_1902 WHERE Year = ?", (year,))
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("No records found.")
    except sqlite3.Error as e:
        print("Error:", e)

def filter_by_event():
    keyword = input("Enter event keyword: ")
    try:
        query = "SELECT * FROM mlb_history_1902 WHERE Event LIKE ?"
        cursor.execute(query, ('%' + keyword + '%',))
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("No matching events found.")
    except sqlite3.Error as e:
        print("Error:", e)

def custom_query():
    sql = input("Enter your SQL query: ")
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except sqlite3.Error as e:
        print("Error:", e)

main_menu()

conn.close()
