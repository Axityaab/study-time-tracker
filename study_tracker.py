import csv
from datetime import datetime, timedelta
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

def calculate_study_streak(sessions):
    study_dates = set()

    for session in sessions:
        date = datetime.strptime(session["date"], "%Y-%m-%d").date()
        study_dates.add(date)

    if not study_dates:
        return 0

    latest_date = max(study_dates)
    today = datetime.now().date()

    if latest_date < today - timedelta(days=1):
        return 0

    streak = 1
    current_date = latest_date - timedelta(days=1)

    while current_date in study_dates:
        streak += 1
        current_date -= timedelta(days=1)

    return streak

def display_subject_chart(subject_totals):
    print("""
=============================
      TIME BY SUBJECT
=============================
""")
    max_minutes = max(subject_totals.values())

    for subject, minutes in subject_totals.items():
        max_minutes = max(subject_totals.values())
        bar_length = max(1, round((minutes / max_minutes) * 25))
        bar = "█" * bar_length

        print(f"{subject:<20} {bar} {minutes} min")

def show_analytics():
    if not DATA_FILE.exists():
        print("""
=============================
        STUDY ANALYTICS
=============================

No study sessions have been recorded yet.
""")
        return

    with DATA_FILE.open("r", newline="") as file:
        reader = csv.DictReader(file)
        sessions = list(reader)

    if not sessions:
        print("""
=============================
        STUDY ANALYTICS
=============================

No study sessions have been recorded yet.
""")
        return

    total_sessions = len(sessions)
    total_minutes = 0
    subject_totals = {}

    for session in sessions:
        duration = int(session["duration"])
        subject = session["subject"]

        total_minutes += duration

        if subject in subject_totals:
            subject_totals[subject] += duration
        else:
            subject_totals[subject] = duration

    average_session = total_minutes / total_sessions

    most_studied_subject = max(
        subject_totals,
        key=subject_totals.get
    )
    study_streak = calculate_study_streak(sessions)
    day_word = "day" if study_streak == 1 else "days"
    print(f"""
=============================
        STUDY ANALYTICS
=============================

Total Sessions: {total_sessions}
Total Study Time: {total_minutes} minutes
Average Session: {average_session:.1f} minutes
Most Studied Subject: {most_studied_subject}
Current Study Streak: {study_streak} {day_word}
""")
    display_subject_chart(subject_totals)

def delete_session():
    if not DATA_FILE.exists():
        print("""
=============================
        DELETE SESSION
=============================

No study sessions have been recorded yet.
""")
        return

    with DATA_FILE.open("r", newline="") as file:
        reader = csv.DictReader(file)
        sessions = list(reader)

    if not sessions:
        print("No study sessions have been recorded yet.")
        return

    print("""
=============================
        DELETE SESSION
=============================
""")

    for number, session in enumerate(sessions, start=1):
        print(
            f"{number}. {session['subject']} - "
            f"{session['duration']} min - {session['date']}"
        )

    while True:
        try:
            choice = int(input("\nEnter the session number to delete: "))

            if choice < 1 or choice > len(sessions):
                print("Invalid session number.")
                continue

            break

        except ValueError:
            print("Please enter a valid number.")

    deleted_session = sessions.pop(choice - 1)

    with DATA_FILE.open("w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["subject", "duration", "date", "notes"])

        for session in sessions:
            writer.writerow([
                session["subject"],
                session["duration"],
                session["date"],
                session["notes"]
            ])

    print(f"\nDeleted: {deleted_session['subject']} - {deleted_session['duration']} minutes")

def weekly_summary():
    if not DATA_FILE.exists():
        print("""
=============================
        WEEKLY SUMMARY
=============================

No study sessions have been recorded yet.
""")
        return

    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    subject_totals = {}
    total_minutes = 0
    session_count = 0

    with DATA_FILE.open("r", newline="") as file:
        reader = csv.DictReader(file)

        for session in reader:
            session_date = datetime.strptime(
                session["date"], "%Y-%m-%d"
            ).date()

            if week_start <= session_date <= week_end:
                subject = session["subject"]
                duration = int(session["duration"])

                if subject in subject_totals:
                    subject_totals[subject] += duration
                else:
                    subject_totals[subject] = duration

                total_minutes += duration
                session_count += 1

    print(f"""
=============================
        WEEKLY SUMMARY
=============================

Week: {week_start} to {week_end}
""")

    if session_count == 0:
        print("No study sessions recorded this week.")
        return

    for subject, minutes in subject_totals.items():
        print(f"{subject}: {minutes} minutes")

    print(f"""
Total Sessions: {session_count}
Total Study Time: {total_minutes} minutes
""")
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
        elif choice == "4":
            weekly_summary()
        elif choice == '6':
            show_analytics()
        elif choice == '7':
            delete_session()

        elif choice == '8':
            print("Goodbye!!")
            break
        
        elif choice == '5':
            print("Features coming soon")
        else:
            print("Invalid choice")

main()