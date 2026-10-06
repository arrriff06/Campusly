import os

from models.student import Student
from utils.file_handler import (
    read_csv,
    append_csv,
    write_csv
)
from utils.validators import (
    validate_student_id,
    validate_name,
    validate_email
)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STUDENT_FILE = os.path.join(BASE_DIR, "data", "students.csv")

STUDENT_FIELDS = [
    "student_id",
    "name",
    "department",
    "email"
]


def initialize_students():
    if not os.path.exists(STUDENT_FILE):
        write_csv(STUDENT_FILE, [], STUDENT_FIELDS)


def get_students():
    return read_csv(STUDENT_FILE)


def student_exists(student_id):
    student_id = student_id.upper()

    students = get_students()

    return any(
        student["student_id"].upper() == student_id
        for student in students
    )


def get_student_by_id(student_id):
    student_id = student_id.upper()

    students = get_students()

    for student in students:
        if student["student_id"].upper() == student_id:
            return student

    return None


def add_student():
    print("\n========== ADD STUDENT ==========")

    try:
        student_id = validate_student_id(
            input("Enter Student ID: ")
        )

        if student_exists(student_id):
            print("Error: Student ID already exists.")
            return

        name = validate_name(
            input("Enter Student Name: ")
        )

        department = validate_name(
            input("Enter Department: ")
        )

        email = validate_email(
            input("Enter Email: ")
        )

        student = Student(
            student_id,
            name,
            department,
            email
        )

        append_csv(
            STUDENT_FILE,
            student.to_dict(),
            STUDENT_FIELDS
        )

        print("\nStudent added successfully.")

    except ValueError as error:
        print(f"\nError: {error}")


def view_students():
    print("\n========== ALL STUDENTS ==========")

    students = get_students()

    if not students:
        print("No students available.")
        return

    for student_data in students:
        student = Student(
            student_data["student_id"],
            student_data["name"],
            student_data["department"],
            student_data["email"]
        )

        student.display()

    print("-" * 70)


def search_student():
    print("\n========== SEARCH STUDENT ==========")

    student_id = input("Enter Student ID: ").strip().upper()

    student = get_student_by_id(student_id)

    if student is None:
        print("Error: Student not found.")
        return

    print("\nStudent Found:")
    print("-" * 70)

    for key, value in student.items():
        print(f"{key.replace('_', ' ').title():20}: {value}")