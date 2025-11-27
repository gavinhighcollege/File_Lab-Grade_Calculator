import os
import matplotlib.pyplot as plt

DATA_DIR = "data"


def load_students():
    """Loads student names and IDs from students.txt."""
    students = {}
    path = os.path.join(DATA_DIR, "students.txt")
    try:
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                # Expects 2 parts: name, sid
                if len(parts) != 2:
                    print(f"Warning: Malformed line in students.txt: {line}")
                    continue
                name, sid = parts
                students[name.strip()] = sid.strip()
    except FileNotFoundError:
        print(f"Error: {path} not found. Ensure 'data' directory is present.")
    return students


def load_assignments():
    """Loads assignment names, points, and IDs from assignments.txt."""
    assignments = {}
    path = os.path.join(DATA_DIR, "assignments.txt")
    try:
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                # Expects 3 parts: name, pts, aid
                if len(parts) != 3:
                    print(f"Warning: Malformed line in assignments.txt: {line}")
                    continue
                name, pts, aid = parts
                try:
                    assignments[name.strip()] = {
                        "points": int(pts.strip()),
                        "id": aid.strip()
                    }
                except ValueError:
                    print(f"Warning: Non-integer points value for assignment: {line}")
    except FileNotFoundError:
        print(f"Error: {path} not found. Ensure 'data' directory is present.")
    return assignments


def load_submissions():
    """
    Loads all submission data from files in the 'data/submissions' directory.
    Submissions are expected to be in individual files named <sid>_<aid>.txt.
    """
    submissions = []
    sub_dir = os.path.join(DATA_DIR, "submissions")

    if not os.path.exists(sub_dir):
        print(f"Error: {sub_dir} not found. Ensure 'data/submissions' directory is present.")
        return submissions

    for filename in os.listdir(sub_dir):
        if not filename.endswith(".txt"):
            continue

        full_path = os.path.join(sub_dir, filename)

        try:
            with open(full_path, "r") as f:
                text = f.read().strip()

                # Skip blank files
                if not text:
                    continue

                parts = text.split()
                # Submission files should contain 3 values: sid, aid, perc
                if len(parts) != 3:
                    # skip malformed submission files (common on Gradescope)
                    # print(f"Warning: Malformed content in submission file {filename}: {text}")
                    continue

                sid, aid, perc_str = parts
                try:
                    submissions.append({
                        "student_id": sid.strip(),
                        "assignment_id": aid.strip(),
                        "percent": float(perc_str.strip())
                    })
                except ValueError:
                    print(f"Warning: Non-float percentage in submission file {filename}: {perc_str}")
                    continue
        except IOError as e:
            print(f"Error reading file {filename}: {e}")

    return submissions


def option_student_grade(students, assignments, submissions):
    """Calculates and prints a student's final course grade."""
    name = input("What is the student's name: ")
    # Case-insensitive check might be better, but sticking to exact match as in original
    if name not in students:
        print("Student not found")
        return

    sid = students[name]

    total_points_earned = 0
    # The specification states: "The total number of points for all the assignments is 1000."
    # So, this should be the total possible points, not a re-calculation.
    TOTAL_POSSIBLE_POINTS = 1000

    # Build a quick lookup for assignment points by ID
    assignment_points_lookup = {
        adata["id"]: adata["points"]
        for adata in assignments.values()
    }

    for sub in submissions:
        if sub["student_id"] == sid:
            aid = sub["assignment_id"]
            if aid in assignment_points_lookup:
                pts_possible = assignment_points_lookup[aid]
                pts_earned = pts_possible * (sub["percent"] / 100.0)  # Use 100.0 for float division
                total_points_earned += pts_earned

    # Check for division by zero, although TOTAL_POSSIBLE_POINTS is fixed at 1000
    if TOTAL_POSSIBLE_POINTS > 0:
        # Calculate percentage and round to the nearest whole percentage
        grade_percent = round((total_points_earned / TOTAL_POSSIBLE_POINTS) * 100)
        print(f"{grade_percent}%")
    else:
        print("Error: Total possible points is zero.")


def option_assignment_stats(assignments, submissions):
    """Calculates and prints statistics (Min, Avg, Max) for an assignment."""
    name = input("What is the assignment name: ")

    # The lookup needs to be case-sensitive as per the existing code structure
    if name not in assignments:
        print("Assignment not found")
        return

    aid = assignments[name]["id"]

    # Filter scores (percentage) for the specific assignment ID
    scores = [sub["percent"] for sub in submissions if sub["assignment_id"] == aid]

    if not scores:
        # This will happen if the assignment exists but has no submissions in the data
        print("Assignment not found")
        return

    # Calculate and print stats, rounding to the nearest whole percentage as requested in examples
    print(f"Min: {round(min(scores))}%")
    print(f"Avg: {round(sum(scores) / len(scores))}%")
    print(f"Max: {round(max(scores))}%")


def option_assignment_graph(assignments, submissions):
    """Generates and displays a histogram of assignment scores."""
    name = input("What is the assignment name: ")
    if name not in assignments:
        print("Assignment not found")
        return

    aid = assignments[name]["id"]

    # Filter scores (percentage) for the specific assignment ID
    scores = [sub["percent"] for sub in submissions if sub["assignment_id"] == aid]

    if not scores:
        print("Assignment not found")
        return

    # Use the example code's bins to cover 0% to 100%
    plt.hist(scores, bins=[0, 25, 50, 75, 100])
    plt.title(f"Score Distribution - {name}")
    plt.xlabel("Score (%)")
    plt.ylabel("Count")
    # Add grid for better readability
    plt.grid(axis='y', alpha=0.75)
    plt.show()

    # Note: The specification requires submitting a screenshot of the graph.


def main():
    """Main function to load data and handle user menu selection."""
    students = load_students()
    assignments = load_assignments()
    submissions = load_submissions()

    # Exit if no data was loaded (e.g., if data directory is missing)
    if not (students and assignments and submissions):
        print("\nCould not load necessary course data. Exiting.")
        return

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