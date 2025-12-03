import sqlite3
from datetime import datetime, timezone

DB_NAME = "posts.db"


def create_post(
    title: str,
    content: str,
    is_published: bool,
    is_active: bool,
    created_at: datetime,
    updated_at: datetime,
    user_id: int,
):
    print("Creating post")
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        sql = """
            INSERT INTO post (title, content, is_published,is_active,created_at,updated_at,user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        cursor.execute(
            sql,
            (title, content, is_published, is_active, created_at, updated_at, user_id),
        )
        conn.commit()
        print("Post created successfully.")


def read_all_posts():
    print("Fetching all posts...")
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM post")
        rows = cursor.fetchall()
        print(f"Fetched {len(rows)} posts.")
        for i, row in enumerate(rows, start=1):
            print(f"Post {i}: {row}")
    return rows


if __name__ == "__main__":
    now = datetime.now(timezone.utc)
    create_post("Post 1", "Post AA-1", False, True, now, now, 2)
    create_post("Post 2", "Post BB-2", False, True, now, now, 3)
    create_post("Post 3", "Post CC-3", False, True, now, now, 2)
    create_post("Post 4", "Post DD-4", False, True, now, now, 3)
    create_post("Post 5", "Post EE-5", False, True, now, now, 2)
    create_post("Post 6", "Post FF-6", False, True, now, now, 3)

    read_all_posts()
