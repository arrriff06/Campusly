import os

from utils.file_handler import (
    read_csv,
    append_csv,
    write_csv
)

from utils.validators import (
    validate_event_id,
    validate_student_id,
    validate_rating
)

from services.event_manager import get_event_by_id
from services.student_manager import get_student_by_id
from services.registration_manager import is_duplicate_registration


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FEEDBACK_FILE = os.path.join(
    BASE_DIR,
    "data",
    "feedback.csv"
)

FEEDBACK_FIELDS = [
    "student_id",
    "event_id",
    "rating",
    "comment"
]


def initialize_feedback():
    if not os.path.exists(FEEDBACK_FILE):
        write_csv(
            FEEDBACK_FILE,
            [],
            FEEDBACK_FIELDS
        )


def get_feedback():
    return read_csv(FEEDBACK_FILE)


def has_submitted_feedback(student_id, event_id):
    feedback = get_feedback()

    for record in feedback:
        if (
            record["student_id"].upper() == student_id.upper()
            and
            record["event_id"].upper() == event_id.upper()
        ):
            return True

    return False


def submit_feedback():
    print("\n========== SUBMIT FEEDBACK ==========")

    try:
        student_id = validate_student_id(
            input("Enter Student ID: ")
        )

        event_id = validate_event_id(
            input("Enter Event ID: ")
        )

        student = get_student_by_id(student_id)

        if student is None:
            raise ValueError("Invalid Student ID.")

        event = get_event_by_id(event_id)

        if event is None:
            raise ValueError("Invalid Event ID.")

        if not is_duplicate_registration(
            student_id,
            event_id
        ):
            raise ValueError(
                "Only registered students can submit feedback."
            )

        if has_submitted_feedback(
            student_id,
            event_id
        ):
            raise ValueError(
                "Feedback has already been submitted."
            )

        rating = validate_rating(
            input("Enter Rating (1-5): ")
        )

        comment = input(
            "Enter Comment (optional): "
        ).strip()

        feedback_record = {
            "student_id": student_id,
            "event_id": event_id,
            "rating": rating,
            "comment": comment
        }

        append_csv(
            FEEDBACK_FILE,
            feedback_record,
            FEEDBACK_FIELDS
        )

        print("\nFeedback submitted successfully.")

    except ValueError as error:
        print(f"\nError: {error}")


def view_feedback():
    print("\n========== ALL FEEDBACK ==========")

    feedback = get_feedback()

    if not feedback:
        print("No feedback available.")
        return

    for record in feedback:
        print("-" * 70)
        print(f"Student ID : {record['student_id']}")
        print(f"Event ID   : {record['event_id']}")
        print(f"Rating     : {record['rating']}")
        print(f"Comment    : {record['comment']}")

    print("-" * 70)