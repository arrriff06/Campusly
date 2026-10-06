from datetime import datetime


def validate_event_id(event_id):
    if not event_id.strip():
        raise ValueError("Event ID cannot be empty.")

    return event_id.strip().upper()


def validate_student_id(student_id):
    if not student_id.strip():
        raise ValueError("Student ID cannot be empty.")

    return student_id.strip().upper()


def validate_name(name):
    if not name.strip():
        raise ValueError("Name cannot be empty.")

    return name.strip()


def validate_email(email):
    email = email.strip()

    if "@" not in email or "." not in email:
        raise ValueError("Invalid email address.")

    return email


def validate_date(date_text):
    date_text = date_text.strip()

    try:
        datetime.strptime(date_text, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format.")

    return date_text


def validate_capacity(capacity):
    try:
        capacity = int(capacity)
    except ValueError:
        raise ValueError("Maximum participants must be a number.")

    if capacity <= 0:
        raise ValueError("Maximum participants must be greater than 0.")

    return capacity


def validate_rating(rating):
    try:
        rating = int(rating)
    except ValueError:
        raise ValueError("Rating must be a number from 1 to 5.")

    if rating < 1 or rating > 5:
        raise ValueError("Rating must be between 1 and 5.")

    return rating