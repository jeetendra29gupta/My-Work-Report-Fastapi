import sqlite3
from datetime import datetime, timezone

DB_NAME = "posts.db"


def create_user(
    full_name: str,
    email_id: str,
    phone_no: str,
    hashed_password: str,
    role: str,
    is_active: bool,
    created_at: datetime,
    updated_at: datetime,
):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        sql = """
            INSERT INTO user (full_name, email_id, phone_no, hashed_password, role, is_active, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(
            sql,
            (
                full_name,
                email_id,
                phone_no,
                hashed_password,
                role,
                is_active,
                created_at,
                updated_at,
            ),
        )
        conn.commit()


def read_all_users():
    print("Fetching all users...")
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user")
        rows = cursor.fetchall()
        print(f"Fetched {len(rows)} users.")
        for i, row in enumerate(rows, start=1):
            print(f"User {i}: {row}")
    return rows


if __name__ == "__main__":
    now = datetime.now(timezone.utc)
    create_user(
        "Jeetendra Gupta",
        "jeetendra29gupta@example.com",
        "9555613730",
        "$2b$12$iklefr.hQ7rOJhgyNHSd1uHm88OQ.5O7U2I5Cr/Xe4exIGzI/MDSa",
        "ADMIN",
        True,
        now,
        now,
    )
    create_user(
        "Sameer Gupta",
        "sameer29gupta@example.com",
        "9555613730",
        "$2b$12$2ixnZronL/FLOhk/YSYGdOl3DY/h/NtZ9.6dqGs63VKjFSwUP7JlC",
        "USER",
        True,
        now,
        now,
    )
    create_user(
        "Prince Gupta",
        "prince29gupta@example.com",
        "9555613730",
        "$2b$12$3dKAylwMcYtNTfMH6tF7vugFQ7XiNYqszkzPe4zC.sL/vDeBg9qye",
        "USER",
        True,
        now,
        now,
    )
    read_all_users()
