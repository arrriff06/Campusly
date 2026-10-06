import os

from models.registration import Registration
from utils.file_handler import (
    read_csv,
    append_csv,
    write_csv
)
from utils.validators import (
    validate_event_id,
    validate_student_id
)

from services.event_manager import get_event_by_id
from services.student_manager import get_student_by_id


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REGISTRATION_FILE = os.path.join(
    BASE_DIR,
    "data",
    "registrations.csv"
)

REGISTRATION_FIELDS = [
    "registration_id",
    "student_id",
    "event_id"
]


def initialize_registrations():
    if not os.path.exists(REGISTRATION_FILE):
        write_csv(
            REGISTRATION_FILE,
            [],
            REGISTRATION_FIELDS
        )


def get_registrations():
    return read_csv(REGISTRATION_FILE)


def generate_registration_id():
    registrations = get_registrations()

    if not registrations:
        return "R001"

    numbers = []

    for registration in registrations:
        registration_id = registration["registration_id"]

        if registration_id.startswith("R"):
            try:
                numbers.append(
                    int(registration_id[1:])
                )
            except ValueError:
                pass

    next_number = max(numbers, default=0) + 1

    return f"R{next_number:03d}"


def is_duplicate_registration(student_id, event_id):
    registrations = get_registrations()

    for registration in registrations:
        if (
            registration["student_id"].upper() == student_id.upper()
            and
            registration["event_id"].upper() == event_id.upper()
        ):
            return True

    return False


def get_event_participant_count(event_id):
    registrations = get_registrations()

    count = 0

    for registration in registrations:
        if registration["event_id"].upper() == event_id.upper():
            count += 1

    return count


def register_student():
    print("\n========== STUDENT REGISTRATION ==========")

    try:
        student_id = validate_student_id(
            input("Enter Student ID: ")
        )

        event_id = validate_event_id(
            input("Enter Event ID: ")
        )

        student = get_student_by_id(student_id)

        if student is None:
            raise ValueError(
                "Invalid Student ID. Student does not exist."
            )

        event = get_event_by_id(event_id)

        if event is None:
            raise ValueError(
                "Invalid Event ID. Event does not exist."
            )

        if is_duplicate_registration(
            student_id,
            event_id
        ):
            raise ValueError(
                "Duplicate registration. "
                "Student is already registered for this event."
            )

        participant_count = get_event_participant_count(
            event_id
        )

        maximum = int(event["max_participants"])

        if participant_count >= maximum:
            raise ValueError(
                "Registration failed. The event is full."
            )

        registration_id = generate_registration_id()

        registration = Registration(
            registration_id,
            student_id,
            event_id
        )

        append_csv(
            REGISTRATION_FILE,
            registration.to_dict(),
            REGISTRATION_FIELDS
        )

        print("\nRegistration successful!")
        print(f"Registration ID: {registration_id}")
        print(f"Student: {student['name']}")
        print(f"Event: {event['event_name']}")

    except ValueError as error:
        print(f"\nError: {error}")


def view_registrations():
    print("\n========== ALL REGISTRATIONS ==========")

    registrations = get_registrations()

    if not registrations:
        print("No registrations available.")
        return

    for registration in registrations:
        print("-" * 60)
        print(
            f"Registration ID : "
            f"{registration['registration_id']}"
        )
        print(
            f"Student ID      : "
            f"{registration['student_id']}"
        )
        print(
            f"Event ID        : "
            f"{registration['event_id']}"
        )

    print("-" * 60)


def search_registered_students():
    print("\n========== SEARCH REGISTERED STUDENTS ==========")

    try:
        event_id = validate_event_id(
            input("Enter Event ID: ")
        )

        event = get_event_by_id(event_id)

        if event is None:
            raise ValueError("Invalid Event ID.")

        registrations = get_registrations()

        matching = [
            registration
            for registration in registrations
            if registration["event_id"].upper() == event_id
        ]

        if not matching:
            print("No students registered for this event.")
            return

        print(f"\nEvent: {event['event_name']}")
        print(f"Total Participants: {len(matching)}")

        print("-" * 70)

        for registration in matching:
            student = get_student_by_id(
                registration["student_id"]
            )

            if student:
                print(
                    f"{student['student_id']} | "
                    f"{student['name']} | "
                    f"{student['department']} | "
                    f"{student['email']}"
                )

    except ValueError as error:
        print(f"\nError: {error}")


def cancel_registration():
    print("\n========== CANCEL REGISTRATION ==========")

    registration_id = input(
        "Enter Registration ID: "
    ).strip().upper()

    registrations = get_registrations()

    new_registrations = [
        registration
        for registration in registrations
        if registration["registration_id"].upper()
        != registration_id
    ]

    if len(registrations) == len(new_registrations):
        print("Error: Registration ID not found.")
        return

    write_csv(
        REGISTRATION_FILE,
        new_registrations,
        REGISTRATION_FIELDS
    )

    print("Registration cancelled successfully.")