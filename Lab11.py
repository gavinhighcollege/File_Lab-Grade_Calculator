import os
import matplotlib.pyplot as plt

DATA_DIR = "data"


def load_students():
    """
    Loads student IDs and names from students.txt.
    Assumes file lines are formatted as: [3-digit ID] [Name] (space separated).
    """
    students = {}
    path = os.path.join(DATA_DIR, "students.txt")
    try:
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                # FIX 1: Use robust whitespace split to separate ID (first part) from Name (remaining parts).
                parts = line.split()

                if len(parts) < 2:
                    continue

                sid = parts[0].strip()
                # Join the rest of the parts back together to form the full name
                name = " ".join(parts[1:]).strip()

                students[name] = sid

    except FileNotFoundError:
        print(f"Error: {path} not found. Ensure 'data' directory is present.")
    return students


def load_assignments():
    """
    Loads assignment data from assignments.txt.
    (Previous fix for 3-line-per-assignment structure is kept, as it resolved the "malformed line" warnings).
    """
    assignments = {}
    path = os.path.join(DATA_DIR, "assignments.txt")

    try:
        with open(path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]

        i = 0
        while i < len(lines):
            if i + 2 >= len(lines):
                break

            name = lines[i]
            aid = lines[i + 1]
            pts_str = lines[i + 2]

            try:
                pts = int(pts_str)
            except ValueError:
                i += 3
                continue

            assignments[name] = {
                "points": pts,
                "id": aid
            }
            i += 3

    except FileNotFoundError:
        print(f"Error: {path} not found. Ensure 'data' directory is present.")
    return assignments


def load_submissions():
    """
    Loads all submission data from files in the 'data/submissions' directory.
    """
    submissions = []
    sub_dir = os.path.join(DATA_DIR, "submissions")

    if not os.path.exists(sub_dir):
        return submissions

    for filename in os.listdir(sub_dir):
        if not filename.endswith(".txt"):
            continue

        full_path = os.path.join(sub_dir, filename)

        try:
            with open(full_path, "r") as f:
                text = f.read().strip()

                if not text:
                    continue

                parts = text.split()
                if len(parts) != 3:
                    continue

                sid, aid, perc_str = parts
                try:
                    submissions.append({
                        # Ensure all IDs and percentage strings are clean
                        "student_id": sid.strip(),
                        "assignment_id": aid.strip(),
                        "percent": float(perc_str.strip())
                    })
                except ValueError:
                    continue
        except IOError as e:
            print(f"Error reading file {filename}: {e}")

    return submissions


def option_student_grade(students, assignments, submissions):
    """Calculates and prints a student's final course grade."""
    # FIX 2: Strip input name to ensure clean dictionary lookup
    name = input("What is the student's name: ").strip()

    if name not in students:
        print("Student not found")
        return

    sid = students[name]

    total_points_earned = 0
    TOTAL_POSSIBLE_POINTS = 1000

    assignment_points_lookup = {
        adata["id"]: adata["points"]
        for adata in assignments.values()
    }

    for sub in submissions:
        # ID comparison must now work because sid and sub["student_id"] are both cleaned strings.
        if sub["student_id"] == sid:
            aid = sub["assignment_id"]
            if aid in assignment_points_lookup:
                pts_possible = assignment_points_lookup[aid]
                pts_earned = pts_possible * (sub["percent"] / 100.0)
                total_points_earned += pts_earned

    if TOTAL_POSSIBLE_POINTS > 0:
        grade_percent = round((total_points_earned / TOTAL_POSSIBLE_POINTS) * 100)
        print(f"{grade_percent}%")
    else:
        print("Error: Total possible points is zero.")


def option_assignment_stats(assignments, submissions):
    """Calculates and prints statistics (Min, Avg, Max) for an assignment."""
    # FIX 3: Strip input assignment name to ensure clean dictionary lookup
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
    print(f"Avg: {round(sum(scores) / len(scores))}%")
    print(f"Max: {round(max(scores))}%")


def option_assignment_graph(assignments, submissions):
    """Generates and displays a histogram of assignment scores."""
    # Strip input assignment name for consistency
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


def main():
    """Main function to load data and handle user menu selection."""
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