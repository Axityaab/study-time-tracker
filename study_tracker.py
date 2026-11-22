import csv
from datetime import datetime
from pathlib import Path

def display_menu():
    print('''
    =============================
         STUDY TIME TRACKER
    =============================

    1. Add Study Session  
    2. View All Sessions  
    3. View Study Summary  
    4. Weekly Summary  
    5. Study Goals  
    6. Analytics  
    7. Delete Session  
    8. Exit
    ''')

DATA_FILE = Path("study_sessions.csv")


def add_study_session():
    print("\n--- Add Study Session ---")

    subject = input("Subject: ").strip()

    if not subject:
        print("Subject cannot be empty.")
        return

    while True:
        try:
            duration = int(input("Duration in minutes: "))

            if duration <= 0:
                print("Duration must be greater than 0.")
                continue

            break

        except ValueError:
            print("Please enter a valid number.")

    while True:
        date_input = input("Date (YYYY-MM-DD) or press Enter for today: ").strip()

        if date_input == "":
            date = datetime.now().strftime("%Y-%m-%d")
            break

        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            date = date_input
            break

        except ValueError:
            print("Invalid date. Use YYYY-MM-DD.")

    notes = input("Notes (optional): ").strip()

    file_exists = DATA_FILE.exists()

    with DATA_FILE.open("a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["subject", "duration", "date", "notes"])

        writer.writerow([subject, duration, date, notes])

    print("Study session saved successfully.")

def main():
    while True:
        display_menu()
        choice = int(input("Choose an option (1-8): "))

        if choice == 1:
            add_study_session()

        if choice == 8:
            print("Goodbye!!")
            break

        elif choice in [2,3,4,5,6,7]:
            print("Features coming soon")
        else:
            print("Invalid choice")

main()