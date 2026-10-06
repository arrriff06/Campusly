import os

import pandas as pd
import matplotlib.pyplot as plt


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FEEDBACK_FILE = os.path.join(
    BASE_DIR,
    "data",
    "feedback.csv"
)

REGISTRATION_FILE = os.path.join(
    BASE_DIR,
    "data",
    "registrations.csv"
)

EVENT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "events.csv"
)

CHART_DIR = os.path.join(
    BASE_DIR,
    "charts"
)


def create_chart_directory():
    if not os.path.exists(CHART_DIR):
        os.makedirs(CHART_DIR)


def load_data():
    try:
        feedback = pd.read_csv(FEEDBACK_FILE)
    except Exception:
        feedback = pd.DataFrame()

    try:
        registrations = pd.read_csv(REGISTRATION_FILE)
    except Exception:
        registrations = pd.DataFrame()

    try:
        events = pd.read_csv(EVENT_FILE)
    except Exception:
        events = pd.DataFrame()

    return feedback, registrations, events


def average_rating_bar_chart():
    feedback, _, events = load_data()

    if feedback.empty:
        print("No feedback data available for chart.")
        return

    feedback["rating"] = pd.to_numeric(
        feedback["rating"],
        errors="coerce"
    )

    result = feedback.groupby(
        "event_id"
    )["rating"].mean()

    if result.empty:
        print("No rating data available.")
        return

    labels = []

    for event_id in result.index:
        name = event_id

        if not events.empty:
            matching = events[
                events["event_id"] == event_id
            ]

            if not matching.empty:
                name = matching.iloc[0]["event_name"]

        labels.append(name)

    plt.figure(figsize=(10, 6))

    plt.bar(labels, result.values)

    plt.xlabel("Events")
    plt.ylabel("Average Rating")
    plt.title("Average Rating by Event")

    plt.ylim(0, 5)

    plt.xticks(
        rotation=30,
        ha="right"
    )

    plt.tight_layout()

    file_path = os.path.join(
        CHART_DIR,
        "event_ratings.png"
    )

    plt.savefig(file_path)
    plt.show()
    plt.close()

    print(
        f"Chart saved successfully:\n{file_path}"
    )


def rating_histogram():
    feedback, _, _ = load_data()

    if feedback.empty:
        print("No feedback data available for chart.")
        return

    ratings = pd.to_numeric(
        feedback["rating"],
        errors="coerce"
    ).dropna()

    if ratings.empty:
        print("No rating data available.")
        return

    plt.figure(figsize=(8, 6))

    plt.hist(
        ratings,
        bins=[0.5, 1.5, 2.5, 3.5, 4.5, 5.5],
        edgecolor="black"
    )

    plt.xlabel("Rating")
    plt.ylabel("Number of Responses")
    plt.title("Rating Distribution")

    plt.xticks([1, 2, 3, 4, 5])

    plt.tight_layout()

    file_path = os.path.join(
        CHART_DIR,
        "rating_distribution.png"
    )

    plt.savefig(file_path)
    plt.show()
    plt.close()

    print(
        f"Chart saved successfully:\n{file_path}"
    )


def event_participation_chart():
    _, registrations, events = load_data()

    if registrations.empty:
        print("No registration data available.")
        return

    result = (
        registrations
        .groupby("event_id")
        .size()
    )

    if result.empty:
        print("No participation data available.")
        return

    labels = []

    for event_id in result.index:
        name = event_id

        if not events.empty:
            matching = events[
                events["event_id"] == event_id
            ]

            if not matching.empty:
                name = matching.iloc[0]["event_name"]

        labels.append(name)

    plt.figure(figsize=(10, 6))

    plt.bar(labels, result.values)

    plt.xlabel("Events")
    plt.ylabel("Number of Participants")
    plt.title("Event-wise Participation")

    plt.xticks(
        rotation=30,
        ha="right"
    )

    plt.tight_layout()

    file_path = os.path.join(
        CHART_DIR,
        "event_participation.png"
    )

    plt.savefig(file_path)
    plt.show()
    plt.close()

    print(
        f"Chart saved successfully:\n{file_path}"
    )