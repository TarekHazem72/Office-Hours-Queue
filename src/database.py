import sqlite3
from pathlib import Path

# Store the database in the project directory.
DATABASE_PATH = Path(__file__).parent / "office_hours.db"


def get_connection():
    """
    Create and return a connection to the SQLite database.
    All other project files should use this function.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row

    # Enable foreign key constraints.
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def initialize_database():
    """
    Create the required database tables if they do not exist.
    This function should run once when the application starts.
    """

    conn = get_connection()
    cursor = conn.cursor()

    # Office-hours sessions.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            instructor_name TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Open'
                CHECK (status IN ('Open', 'Closed')),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            closed_at DATETIME
        )
    """)

    # Students registered in each session.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS queue_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            student_name TEXT NOT NULL,
            topic TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Waiting'
                CHECK (status IN ('Waiting', 'Called', 'Done', 'Left')),
            joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (session_id)
                REFERENCES sessions(id)
                ON DELETE CASCADE
        )
    """)

    # Prevent duplicate active entries for the same student
    # in the same session.
    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS
        unique_active_student_entry
        ON queue_entries(session_id, student_name)
        WHERE status IN ('Waiting', 'Called')
    """)

    conn.commit()
    conn.close()

    print("Database initialized successfully.")


if __name__ == "__main__":
    initialize_database()
