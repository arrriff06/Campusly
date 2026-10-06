import os

from models.event import Event
from utils.file_handler import (
    read_csv,
    append_csv,
    write_csv
)
from utils.validators import (
    validate_event_id,
    validate_name,
    validate_date,
    validate_capacity
)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVENT_FILE = os.path.join(BASE_DIR, "data", "events.csv")

EVENT_FIELDS = [
    "event_id",
    "event_name",
    "date",
    "venue",
    "max_participants"
]


def initialize_events():
    if not os.path.exists(EVENT_FILE):
        write_csv(EVENT_FILE, [], EVENT_FIELDS)


def get_events():
    return read_csv(EVENT_FILE)


def event_exists(event_id):
    event_id = event_id.upper()

    events = get_events()

    return any(
        event["event_id"].upper() == event_id
        for event in events
    )


def get_event_by_id(event_id):
    event_id = event_id.upper()

    events = get_events()

    for event in events:
        if event["event_id"].upper() == event_id:
            return event

    return None


def create_event():
    print("\n========== CREATE EVENT ==========")

    try:
        event_id = validate_event_id(
            input("Enter Event ID: ")
        )

        if event_exists(event_id):
            print("Error: Event ID already exists.")
            return

        event_name = validate_name(
            input("Enter Event Name: ")
        )

        date = validate_date(
            input("Enter Date (YYYY-MM-DD): ")
        )

        venue = validate_name(
            input("Enter Venue: ")
        )

        max_participants = validate_capacity(
            input("Enter Maximum Participants: ")
        )

        event = Event(
            event_id,
            event_name,
            date,
            venue,
            max_participants
        )

        append_csv(
            EVENT_FILE,
            event.to_dict(),
            EVENT_FIELDS
        )

        print("\nEvent created successfully.")

    except ValueError as error:
        print(f"\nError: {error}")


def view_events():
    print("\n========== ALL EVENTS ==========")

    events = get_events()

    if not events:
        print("No events available.")
        return

    for event_data in events:
        event = Event(
            event_data["event_id"],
            event_data["event_name"],
            event_data["date"],
            event_data["venue"],
            event_data["max_participants"]
        )

        event.display()

    print("-" * 70)


def search_event():
    print("\n========== SEARCH EVENT ==========")

    event_id = input("Enter Event ID: ").strip().upper()

    event = get_event_by_id(event_id)

    if event is None:
        print("Error: Invalid Event ID.")
        return

    print("\nEvent Found:")
    print("-" * 70)

    for key, value in event.items():
        print(f"{key.replace('_', ' ').title():22}: {value}")


def update_event():
    print("\n========== UPDATE EVENT ==========")

    event_id = input("Enter Event ID to update: ").strip().upper()

    events = get_events()

    found = False

    for event in events:
        if event["event_id"].upper() == event_id:
            found = True

            print("Press Enter to keep the existing value.")

            name = input(
                f"Event Name [{event['event_name']}]: "
            ).strip()

            date = input(
                f"Date [{event['date']}]: "
            ).strip()

            venue = input(
                f"Venue [{event['venue']}]: "
            ).strip()

            capacity = input(
                f"Maximum Participants [{event['max_participants']}]: "
            ).strip()

            if name:
                event["event_name"] = validate_name(name)

            if date:
                event["date"] = validate_date(date)

            if venue:
                event["venue"] = validate_name(venue)

            if capacity:
                event["max_participants"] = str(
                    validate_capacity(capacity)
                )

            break

    if not found:
        print("Error: Invalid Event ID.")
        return

    write_csv(EVENT_FILE, events, EVENT_FIELDS)

    print("Event updated successfully.")


def delete_event():
    print("\n========== DELETE EVENT ==========")

    event_id = input("Enter Event ID to delete: ").strip().upper()

    events = get_events()

    new_events = [
        event for event in events
        if event["event_id"].upper() != event_id
    ]

    if len(events) == len(new_events):
        print("Error: Invalid Event ID.")
        return

    write_csv(EVENT_FILE, new_events, EVENT_FIELDS)

    print("Event deleted successfully.")