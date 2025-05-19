from datetime import datetime

# Subjects and teachers
subject = {
    'psp': {'lecture': 0, 'date': [], 'slot': [], 'name': 'Vansh'},
    'fds': {'lecture': 0, 'date': [], 'slot': [], 'name': 'Aadi'},
    'maths': {'lecture': 0, 'date': [], 'slot': [], 'name': 'Shakti'}
}

# Students
student = {
    73: {'psp': 0, 'fds': 0, 'maths': 0},
    74: {'psp': 0, 'fds': 0, 'maths': 0},
    75: {'psp': 0, 'fds': 0, 'maths': 0},
    76: {'psp': 0, 'fds': 0, 'maths': 0},
    77: {'psp': 0, 'fds': 0, 'maths': 0}
}

attendance_record = {sid: {'psp': [], 'fds': [], 'maths': []} for sid in student}
lecture_log = set()

def mark_attendance():
    while True:
        subject_name = input("Enter Subject (psp/fds/maths): ").strip().lower()
        if subject_name in subject:
            break
        print("Invalid subject. Please enter psp, fds, or maths.")

    while True:
        date_input = input("Enter Date and Time (YYYY-MM-DD HH:MM): ").strip()
        try:
            date_obj = datetime.strptime(date_input, '%Y-%m-%d %H:%M')
            formatted_date = date_obj.strftime('%Y-%m-%d %H:%M')
            break
        except ValueError:
            print("Invalid date format. Try again.")

    lecture_key = f"{subject_name}-{formatted_date}"
    if lecture_key in lecture_log:
        print("Attendance already marked for this lecture.")
        return

    subject[subject_name]['lecture'] += 1
    lecture_no = subject[subject_name]['lecture']
    subject[subject_name]['date'].append(formatted_date)
    subject[subject_name]['slot'].append(f"Lecture {lecture_no}")
    lecture_log.add(lecture_key)

    while True:
        absent_input = input("Enter absent roll numbers separated by space: ").strip()
        try:
            absent_rolls = set(map(int, absent_input.split())) if absent_input else set()
            if all(sid in student for sid in absent_rolls):
                break
            else:
                raise ValueError
        except ValueError:
            print("Invalid input. Please enter valid roll numbers.")

    for sid in student:
        if sid in absent_rolls:
            attendance_record[sid][subject_name].append((lecture_no, formatted_date, "Absent"))
        else:
            student[sid][subject_name] += 1
            attendance_record[sid][subject_name].append((lecture_no, formatted_date, "Present"))

    print("Attendance marked successfully.\n")

def view_overall_attendance():
    print("\nOverall Attendance for All Subjects (%):\n")
    for sid in sorted(student):
        total_present = sum(student[sid][subj] for subj in subject)
        total_lectures = sum(subject[subj]['lecture'] for subj in subject)
        percent = (total_present / total_lectures * 100) if total_lectures else 0
        print(f"Student {sid}: {total_present}/{total_lectures} Present ({percent:.2f}%)")

def view_subjectwise_attendance_percent():
    print("\nSubject-wise Attendance (%):")
    for subj in subject:
        print(f"\nSubject: {subj.upper()}")
        total_lectures = subject[subj]['lecture']
        for sid in sorted(student):
            present = student[sid][subj]
            percent = (present / total_lectures * 100) if total_lectures else 0
            print(f"  Student {sid}: {present}/{total_lectures} Present ({percent:.2f}%)")

def edit_attendance():
    while True:
        try:
            sid = int(input("Enter student roll number to edit: "))
            if sid in student:
                break
            else:
                print("Roll number not found.")
        except ValueError:
            print("Invalid input. Enter a valid number.")

    while True:
        subj = input("Enter subject (psp/fds/maths): ").strip().lower()
        if subj in subject:
            break
        print("Invalid subject. Try again.")

    records = attendance_record[sid][subj]
    if not records:
        print("No attendance records for this student in this subject.")
        return

    for i, (lec_no, date, status) in enumerate(records):
        print(f"{i+1}. Lecture {lec_no} - {date} - {status}")

    while True:
        try:
            idx = int(input("Enter lecture number to change attendance ")) - 1
            if 0 <= idx < len(records):
                lec_no, date, status = records[idx]
                new_status = "Absent" if status == "Present" else "Present"
                records[idx] = (lec_no, date, new_status)
                student[sid][subj] += 1 if new_status == "Present" else -1
                print("Attendance updated.")
                break
            else:
                print("Invalid index.")
        except ValueError:
            print("Enter a valid number.")

def view_overall_detention():
    print("\nOverall Detention List (<75% Attendance):")
    for sid in sorted(student):
        total_present = sum(student[sid][subj] for subj in subject)
        total_lectures = sum(subject[subj]['lecture'] for subj in subject)
        if total_lectures == 0:
            continue
        percent = (total_present / total_lectures) * 100
        if percent < 75:
            print(f"Student {sid}: {percent:.2f}%")

def view_subjectwise_detention():
    print("\nSubject-wise Detention List (<75% Attendance):")
    for subj in subject:
        print(f"\nSubject: {subj.upper()}")
        total_lectures = subject[subj]['lecture']
        for sid in sorted(student):
            if total_lectures == 0:
                continue
            percent = (student[sid][subj] / total_lectures) * 100
            if percent < 75:
                print(f"  Student {sid}: {percent:.2f}%")

# Main menu loop
while True:
    print("\nClassroom Attendance Tracker")
    print("1. Mark Attendance")
    print("2. View Overall Attendance in %")
    print("3. View Subject-wise Attendance in %")
    print("4. Edit Attendance")
    print("5. View Overall Detention List (<75%)")
    print("6. View Subject-wise Detention List (<75%)")
    print("7. Exit")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        mark_attendance()
    elif choice == "2":
        view_overall_attendance()
    elif choice == "3":
        view_subjectwise_attendance_percent()
    elif choice == "4":
        edit_attendance()
    elif choice == "5":
        view_overall_detention()
    elif choice == "6":
        view_subjectwise_detention()
    elif choice == "7":
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please try again.")