import json
import sqlite3

DB_NAME = "work-report.db"


def read_all_posts():
    print("Fetching all records...")
    json_data = []  # ← move list here so it resets each run

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        rows = cursor.fetchall()

        for row in rows:
            json_data.append({
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "note": row[3]
            })

    with open("tasks.json", "w") as f:
        json.dump({"tasks": json_data}, f, indent=4)


if __name__ == "__main__":
    read_all_posts()
