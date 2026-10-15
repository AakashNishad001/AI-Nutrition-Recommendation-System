"""SQLite storage for optional feedback/history."""

from pathlib import Path
import sqlite3
from datetime import datetime


def get_connection(db_path="database/app.db"):
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(path)


def initialize_database(db_path="database/app.db"):
    with get_connection(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                food_name TEXT NOT NULL,
                rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
                comment TEXT,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()


def save_feedback(food_name, rating, comment="", db_path="database/app.db"):
    with get_connection(db_path) as conn:
        conn.execute(
            "INSERT INTO feedback (food_name, rating, comment, created_at) VALUES (?, ?, ?, ?)",
            (food_name, int(rating), comment, datetime.now().isoformat(timespec="seconds"))
        )
        conn.commit()


def get_feedback(db_path="database/app.db"):
    with get_connection(db_path) as conn:
        return conn.execute(
            "SELECT id, food_name, rating, comment, created_at "
            "FROM feedback ORDER BY id DESC"
        ).fetchall()
