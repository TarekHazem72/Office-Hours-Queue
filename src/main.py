
from database import initialize_database

# Import functions written by the other team members.
from session_management import open_session, close_session
from student_queue import join_queue
from queue_display import get_queue
from instructor_controls import call_next, mark_done


def display_menu():
    print("\n" + "=" * 35)
    print("       OFFICE HOURS QUEUE")
    print("=" * 35)
    print("1. Open office-hours session")
    print("2. Close office-hours session")
    print("3. Join queue")
    print("4. View queue")
    print("5. Call next student")
    print("6. Mark student as done")
    print("7. Exit")
    print("=" * 35)


def open_session_menu():
    instructor = input("Enter instructor name: ").strip()

    if not instructor:
        print("Instructor name cannot be empty.")
        return

    success, message = open_session(instructor)
    print(message)


def close_session_menu():
    success, message = close_session()
    print(message)


def join_queue_menu():
    student = input("Enter student name: ").strip()
    topic = input("Enter your question/topic: ").strip()

    if not student or not topic:
        print("Both name and topic are required.")
        return

    success, message = join_queue(student, topic)
    print(message)


def view_queue_menu():
    queue = get_queue()

    if not queue:
        print("The queue is currently empty.")
        return

    print("\nCURRENT QUEUE")
    print("-" * 50)

    for student in queue:
        print(
            f"Position: {student['position']} | "
            f"Name: {student['student_name']} | "
            f"Topic: {student['topic']} | "
            f"Status: {student['status']}"
        )

    print("-" * 50)


def call_next_menu():
    success, message = call_next()
    print(message)


def mark_done_menu():
    entry_id = input("Enter the queue entry ID: ").strip()

    if not entry_id.isdigit():
        print("Please enter a valid entry ID.")
        return

    success, message = mark_done(int(entry_id))
    print(message)


def main():
    # Create database tables before starting the application.
    initialize_database()

    print("\nWelcome to the Office Hours Queue System!")

    while True:
        display_menu()

        choice = input("Select an option (1-7): ").strip()

        if choice == "1":
            open_session_menu()

        elif choice == "2":
            close_session_menu()

        elif choice == "3":
            join_queue_menu()

        elif choice == "4":
            view_queue_menu()

        elif choice == "5":
            call_next_menu()

        elif choice == "6":
            mark_done_menu()

        elif choice == "7":
            print("Thank you for using the Office Hours Queue System.")
            break

        else:
            print("Invalid option. Please select a number between 1 and 7.")


if __name__ == "__main__":
    main()
