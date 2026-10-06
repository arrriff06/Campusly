import os

from services.event_manager import (
    initialize_events,
    create_event,
    view_events,
    search_event,
    update_event,
    delete_event
)

from services.student_manager import (
    initialize_students,
    add_student,
    view_students,
    search_student
)

from services.registration_manager import (
    initialize_registrations,
    register_student,
    view_registrations,
    search_registered_students,
    cancel_registration
)

from services.feedback_manager import (
    initialize_feedback,
    submit_feedback,
    view_feedback
)

from analysis.feedback_analyzer import (
    average_rating,
    total_participants,
    event_wise_participation,
    highest_rated_event,
    rating_distribution,
    overall_statistics
)

from visualization.charts import (
    create_chart_directory,
    average_rating_bar_chart,
    rating_histogram,
    event_participation_chart
)


def initialize_application():
    """Initialize required files and folders."""

    os.makedirs(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "data"
        ),
        exist_ok=True
    )

    os.makedirs(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "charts"
        ),
        exist_ok=True
    )

    initialize_events()
    initialize_students()
    initialize_registrations()
    initialize_feedback()
    create_chart_directory()


def event_management_menu():

    while True:
        print("\n")
        print("=" * 55)
        print("              EVENT MANAGEMENT")
        print("=" * 55)

        print("1. Create Event")
        print("2. View All Events")
        print("3. Search Event")
        print("4. Update Event")
        print("5. Delete Event")
        print("6. Back to Main Menu")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            create_event()

        elif choice == "2":
            view_events()

        elif choice == "3":
            search_event()

        elif choice == "4":
            update_event()

        elif choice == "5":
            delete_event()

        elif choice == "6":
            break

        else:
            print("Invalid choice. Please try again.")


def student_management_menu():

    while True:
        print("\n")
        print("=" * 55)
        print("              STUDENT MANAGEMENT")
        print("=" * 55)

        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Back to Main Menu")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            add_student()

        elif choice == "2":
            view_students()

        elif choice == "3":
            search_student()

        elif choice == "4":
            break

        else:
            print("Invalid choice. Please try again.")


def registration_menu():

    while True:
        print("\n")
        print("=" * 55)
        print("              EVENT REGISTRATION")
        print("=" * 55)

        print("1. Register Student")
        print("2. View All Registrations")
        print("3. Search Registered Students")
        print("4. Cancel Registration")
        print("5. Back to Main Menu")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            register_student()

        elif choice == "2":
            view_registrations()

        elif choice == "3":
            search_registered_students()

        elif choice == "4":
            cancel_registration()

        elif choice == "5":
            break

        else:
            print("Invalid choice. Please try again.")


def feedback_menu():

    while True:
        print("\n")
        print("=" * 55)
        print("              FEEDBACK MANAGEMENT")
        print("=" * 55)

        print("1. Submit Feedback")
        print("2. View All Feedback")
        print("3. Back to Main Menu")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            submit_feedback()

        elif choice == "2":
            view_feedback()

        elif choice == "3":
            break

        else:
            print("Invalid choice. Please try again.")


def analysis_menu():

    while True:
        print("\n")
        print("=" * 55)
        print("              FEEDBACK ANALYSIS")
        print("=" * 55)

        print("1. Average Rating")
        print("2. Total Participants")
        print("3. Event-wise Participation")
        print("4. Highest Rated Event")
        print("5. Rating Distribution")
        print("6. Overall Statistics")
        print("7. Back to Main Menu")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            average_rating()

        elif choice == "2":
            total_participants()

        elif choice == "3":
            event_wise_participation()

        elif choice == "4":
            highest_rated_event()

        elif choice == "5":
            rating_distribution()

        elif choice == "6":
            overall_statistics()

        elif choice == "7":
            break

        else:
            print("Invalid choice. Please try again.")


def visualization_menu():

    while True:
        print("\n")
        print("=" * 55)
        print("              DATA VISUALIZATION")
        print("=" * 55)

        print("1. Average Rating Bar Chart")
        print("2. Rating Histogram")
        print("3. Event Participation Graph")
        print("4. Back to Main Menu")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            average_rating_bar_chart()

        elif choice == "2":
            rating_histogram()

        elif choice == "3":
            event_participation_chart()

        elif choice == "4":
            break

        else:
            print("Invalid choice. Please try again.")


def main():

    initialize_application()

    while True:

        print("\n")
        print("=" * 65)
        print("        CAMPUS EVENT MANAGEMENT & FEEDBACK ANALYZER")
        print("=" * 65)

        print("1. Event Management")
        print("2. Student Management")
        print("3. Event Registration")
        print("4. Feedback Management")
        print("5. Feedback Analysis")
        print("6. Data Visualization")
        print("7. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            event_management_menu()

        elif choice == "2":
            student_management_menu()

        elif choice == "3":
            registration_menu()

        elif choice == "4":
            feedback_menu()

        elif choice == "5":
            analysis_menu()

        elif choice == "6":
            visualization_menu()

        elif choice == "7":
            print("\nThank you for using Campus Event Management System.")
            print("Program terminated.")
            break

        else:
            print("\nInvalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()