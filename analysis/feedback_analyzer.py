import os

import numpy as np
import pandas as pd


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


def load_feedback():
    if not os.path.exists(FEEDBACK_FILE):
        return pd.DataFrame()

    try:
        df = pd.read_csv(FEEDBACK_FILE)

        if df.empty:
            return df

        df["rating"] = pd.to_numeric(
            df["rating"],
            errors="coerce"
        )

        return df

    except Exception:
        return pd.DataFrame()


def load_registrations():
    if not os.path.exists(REGISTRATION_FILE):
        return pd.DataFrame()

    try:
        return pd.read_csv(REGISTRATION_FILE)
    except Exception:
        return pd.DataFrame()


def load_events():
    if not os.path.exists(EVENT_FILE):
        return pd.DataFrame()

    try:
        return pd.read_csv(EVENT_FILE)
    except Exception:
        return pd.DataFrame()


def average_rating():
    print("\n========== AVERAGE EVENT RATING ==========")

    df = load_feedback()

    if df.empty:
        print("No feedback data available.")
        return

    result = (
        df.groupby("event_id")["rating"]
        .mean()
        .round(2)
    )

    events = load_events()

    for event_id, rating in result.items():

        event_name = event_id

        if not events.empty:
            matching = events[
                events["event_id"] == event_id
            ]

            if not matching.empty:
                event_name = matching.iloc[0]["event_name"]

        print(
            f"{event_id} - {event_name}: "
            f"{rating}/5"
        )


def total_participants():
    print("\n========== TOTAL PARTICIPANTS ==========")

    df = load_registrations()

    if df.empty:
        print("No registration data available.")
        return

    total = len(df)

    print(f"Total registrations: {total}")


def event_wise_participation():
    print("\n========== EVENT-WISE PARTICIPATION ==========")

    registrations = load_registrations()

    if registrations.empty:
        print("No registration data available.")
        return

    result = (
        registrations
        .groupby("event_id")
        .size()
        .sort_values(ascending=False)
    )

    events = load_events()

    for event_id, count in result.items():

        event_name = event_id

        if not events.empty:
            matching = events[
                events["event_id"] == event_id
            ]

            if not matching.empty:
                event_name = matching.iloc[0]["event_name"]

        print(
            f"{event_id} - {event_name}: "
            f"{count} participants"
        )


def highest_rated_event():
    print("\n========== HIGHEST RATED EVENT ==========")

    df = load_feedback()

    if df.empty:
        print("No feedback data available.")
        return

    average_ratings = (
        df.groupby("event_id")["rating"]
        .mean()
    )

    highest_event = average_ratings.idxmax()
    highest_rating = average_ratings.max()

    events = load_events()

    event_name = highest_event

    if not events.empty:
        matching = events[
            events["event_id"] == highest_event
        ]

        if not matching.empty:
            event_name = matching.iloc[0]["event_name"]

    print(f"Event: {event_name}")
    print(f"Event ID: {highest_event}")
    print(f"Average Rating: {highest_rating:.2f}/5")


def rating_distribution():
    print("\n========== RATING DISTRIBUTION ==========")

    df = load_feedback()

    if df.empty:
        print("No feedback data available.")
        return

    ratings = df["rating"].dropna().to_numpy()

    if len(ratings) == 0:
        print("No valid ratings available.")
        return

    rating_array = np.array(ratings)

    for rating in range(1, 6):
        count = np.sum(rating_array == rating)

        print(
            f"Rating {rating}: "
            f"{count} response(s)"
        )


def overall_statistics():
    print("\n========== OVERALL FEEDBACK STATISTICS ==========")

    df = load_feedback()

    if df.empty:
        print("No feedback data available.")
        return

    ratings = df["rating"].dropna().to_numpy()

    if len(ratings) == 0:
        print("No ratings available.")
        return

    rating_array = np.array(ratings)

    print(f"Number of Feedback Responses: {len(rating_array)}")
    print(
        f"Average Rating: "
        f"{np.mean(rating_array):.2f}"
    )
    print(
        f"Highest Rating: "
        f"{np.max(rating_array)}"
    )
    print(
        f"Lowest Rating: "
        f"{np.min(rating_array)}"
    )
    