import csv
import os


def ensure_file(file_path, fieldnames):
    """Create a CSV file with headers if it does not exist."""
    directory = os.path.dirname(file_path)

    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()


def read_csv(file_path):
    """Read all records from a CSV file."""
    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def write_csv(file_path, data, fieldnames):
    """Overwrite a CSV file with the given data."""
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def append_csv(file_path, data, fieldnames):
    """Append one record to a CSV file."""
    file_exists = os.path.exists(file_path) and os.path.getsize(file_path) > 0

    with open(file_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(data)


def delete_record(file_path, key, value, fieldnames):
    """Delete records matching a key-value pair."""
    data = read_csv(file_path)

    new_data = [
        row for row in data
        if row.get(key) != value
    ]

    write_csv(file_path, new_data, fieldnames)

    return len(data) != len(new_data)