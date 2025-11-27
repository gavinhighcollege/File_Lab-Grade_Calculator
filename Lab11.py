import os
import matplotlib.pyplot as plt

DATA_DIR = "data"


# ---------------------------------------------------------
# LOAD STUDENTS
# ---------------------------------------------------------
def load_students():
    """
    Loads student IDs and names from students.txt.
    Format example:
    174Michael Potter
    """
    students = {}
    path = os.path.join(DATA_DIR, "students.txt")

    try:
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if len(line) < 4:
                    continue

                sid = line[:3]               # first 3 chars = ID
                name = line[3:].strip()      # remainder = name

                students[name] = sid

    except FileNotFoundError:
        print("students.txt not found")

    return students


# ---------------------------------------------------------
# LOAD ASSIGNMENTS
# ---------------------------------------------------------
def load_assignments():
    """
    Loads assignment names, IDs, and points.
    Each assignment is 3 lines:
    Name
    ID
    Points
    """
    assignments = {}
    path = os.path.join(DATA_DIR, "assignments.txt")

    try:
        with open(path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]

        i = 0
        while i < len(lines):
            name = lines[i]
            aid = lines[i + 1]
            pts = int(lines[i + 2])

            assignments[name] = {
                "id": aid,
                "points": pts
            }

            i += 3

    except FileNotFoundError:
        print("assignments.txt not found")

    return assignments


# ---------------------------------------------------------
# LOAD SUBMISSIONS
# ---------------------------------------------------------
def load_submissions():
    """
    Loads submission files.
    Format inside each file:
    SID|AID|PERCENT
    """
    submissions = []
    sub_dir = os.path.join(DATA_DIR, "submissions")

    if not os.path.exists(sub_dir):
        return submissions

    for filename in os.listdir(sub_dir):
        if not filename.endswith(".txt"):
            continue

        full_path = os.path.join(sub_dir, filename)

        with open(full_path, 'r') as f:
            text = f.read().strip()
            if not text:
                continue

            parts = text.split("|")
            if len(parts) != 3:
                continue

            sid, aid, perc = parts

            submissions.append({
                "student_id": sid.strip(),
                "assignment_id": aid.strip(),
                "percent": float(perc.strip())
            })

    return submissions


# ---------------------------------------------------------
# OPTION 1: STUDENT GRADE
# ---------------------------------------------------------
def option_student_grade(students, assignments, submissions):
    name = input("What is the student's name: ").strip()

    if name not in students:
        print("Student not found")
        return

    sid = students[name]

    TOTAL_POSSIBLE = 1000
    total_earned = 0

    # lookup table: assignment_id → points
    points_for_id = {adata["id"]: adata["points"] for adata in assignments.values()}

    for sub in submissions:
        if sub["student_id"] == sid:
            aid = sub["assignment_id"]
            if aid in points_for_id:
                pts = points_for_id[aid]
                earned = pts * (sub["percent"] / 100)
                total_earned += earned

    grade_percent = round((total_earned / TOTAL_POSSIBLE) * 100)
    print(f"{grade_percent}%")


# ---------------------------------------------------------
# OPTION 2: ASSIGNMENT STATS
# ---------------------------------------------------------
def option_assignment_stats(assignments, submissions):
    name = input("What is the assignment name: ").strip()

    if name not in assignments:
        print("Assignment not found")
        return

    aid = assignments[name]["id"]

    scores = [sub["percent"] for sub in submissions if sub["assignment_id"] == aid]

    if not scores:
        print("Assignment not found")
        return

    print(f"Min: {round(min(scores))}%")
    avg = sum(scores) / len(scores)
    avg_int = int(avg)  # floors toward zero
    print(f"Avg: {avg_int}%")
    print(f"Max: {round(max(scores))}%")


# ---------------------------------------------------------
# OPTION 3: ASSIGNMENT HISTOGRAM
# ---------------------------------------------------------
def option_assignment_graph(assignments, submissions):
    name = input("What is the assignment name: ").strip()

    if name not in assignments:
        print("Assignment not found")
        return

    aid = assignments[name]["id"]

    scores = [sub["percent"] for sub in submissions if sub["assignment_id"] == aid]

    if not scores:
        print("Assignment not found")
        return

    plt.hist(scores, bins=[0, 25, 50, 75, 100])
    plt.title(f"Score Distribution - {name}")
    plt.xlabel("Score (%)")
    plt.ylabel("Count")
    plt.show()


# ---------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------
def main():
    students = load_students()
    assignments = load_assignments()
    submissions = load_submissions()

    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph\n")

    choice = input("Enter your selection: ")

    if choice == "1":
        option_student_grade(students, assignments, submissions)
    elif choice == "2":
        option_assignment_stats(assignments, submissions)
    elif choice == "3":
        option_assignment_graph(assignments, submissions)
    else:
        print("Invalid option")


if __name__ == "__main__":
    main()
