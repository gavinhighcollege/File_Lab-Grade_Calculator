import os
import matplotlib.pyplot as plt

DATA_DIR = "data"


def load_students():
    students = {}
    path = os.path.join(DATA_DIR, "students.txt")
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) != 2:
                continue
            name, sid = parts
            students[name] = sid
    return students


def load_assignments():
    assignments = {}
    path = os.path.join(DATA_DIR, "assignments.txt")
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) != 3:
                continue
            name, pts, aid = parts
            assignments[name] = {
                "points": int(pts),
                "id": aid
            }
    return assignments



def load_submissions():
    submissions = []   # list of dicts
    sub_dir = os.path.join(DATA_DIR, "submissions")

    for filename in os.listdir(sub_dir):
        if not filename.endswith(".txt"):
            continue

        with open(os.path.join(sub_dir, filename), "r") as f:
            text = f.read().strip()
            if not text:
                continue

            sid, aid, perc = text.split()
            submissions.append({
                "student_id": sid,
                "assignment_id": aid,
                "percent": float(perc)
            })

    return submissions

def option_student_grade(students, assignments, submissions):
    name = input("What is the student's name: ")
    if name not in students:
        print("Student not found")
        return

    sid = students[name]

    total_points_earned = 0
    total_points_possible = 1000

    for sub in submissions:
        if sub["student_id"] == sid:
            # find assignment's point value
            for aname, adata in assignments.items():
                if adata["id"] == sub["assignment_id"]:
                    pts_possible = adata["points"]
                    pts_earned = pts_possible * (sub["percent"] / 100)
                    total_points_earned += pts_earned

    grade_percent = round((total_points_earned / total_points_possible) * 100)
    print(f"{grade_percent}%")


def option_assignment_stats(assignments, submissions):
    name = input("What is the assignment name: ")
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
    name = input("What is the assignment name: ")
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




