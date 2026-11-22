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

def view_all_sessions():
    if not DATA_FILE.exists():
        print('''
        =============================
             NO STUDY SESSIONS
        =============================
        No study sessions have been recorded yet.
        ''')
        return

    with DATA_FILE.open("r", newline="") as file:
        reader = csv.DictReader(file)
        sessions = list(reader)

    if not sessions:
        print('''
        =============================
             NO STUDY SESSIONS
        =============================
        No study sessions have been recorded yet.
        ''')
        return

    print('''
    =============================
          ALL STUDY SESSIONS
    =============================
    ''')

    for number, session in enumerate(sessions, start=1):
        print(f"""
    Session {number}
    -----------------------------
    Subject: {session["subject"]}
    Duration: {session["duration"]} minutes
    Date: {session["date"]}
    Notes: {session["notes"] if session["notes"] else "None"}
    """)
def view_study_summary():
    if not DATA_FILE.exists():
        print("""
=============================
      STUDY SUMMARY
=============================

No study sessions have been recorded yet.
""")
        return

    totals = {}
    total_minutes = 0

    with DATA_FILE.open("r", newline="") as file:
        reader = csv.DictReader(file)

        for session in reader:
            subject = session["subject"]
            duration = int(session["duration"])

            if subject in totals:
                totals[subject] += duration
            else:
                totals[subject] = duration

            total_minutes += duration

    if not totals:
        print("""
=============================
      STUDY SUMMARY
=============================

No study sessions have been recorded yet.
""")
        return

    print("""
=============================
      STUDY SUMMARY
=============================
""")

    for subject, minutes in totals.items():
        print(f"{subject}: {minutes} minutes")

    print(f"\nTotal Study Time: {total_minutes} minutes")
def main():
    while True:
        display_menu()
        choice = input("Choose an option (1-8): ").strip()

        if choice == '1':
            add_study_session()

        elif choice == '2':
            view_all_sessions()

        elif choice == '3':
            view_study_summary()

        elif choice == '8':
            print("Goodbye!!")
            break

        elif choice in ['4','5','6','7']:
            print("Features coming soon")
        else:
            print("Invalid choice")

main()