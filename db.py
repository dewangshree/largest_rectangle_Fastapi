import sqlite3

DB_PATH = "logs.db"

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    """Creates the logs table if it doesn't exist."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input TEXT NOT NULL,
                output TEXT NOT NULL,
                time_taken REAL NOT NULL
            )
        """)

init_db()