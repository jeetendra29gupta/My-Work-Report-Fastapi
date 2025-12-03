import sqlite3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

DB_PATH = "user-database.db"

app = FastAPI(title="FastAPI + SQLite (No ORM)")


# --- Database Helpers ---
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Return dict-like rows
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# --- Initialize DB on app startup ---
init_db()


# --- Pydantic Model ---
class User(BaseModel):
    name: str
    email: str


# --- Routes ---
@app.post("/users/")
def create_user(user: User):
    conn = get_db_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)", (user.name, user.email)
        )
        conn.commit()
        user_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already exists")
    finally:
        conn.close()
    return {"id": user_id, "message": "User created successfully"}


@app.get("/users/")
def list_users():
    conn = get_db_connection()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return [dict(u) for u in users]


@app.get("/users/{user_id}")
def get_user(user_id: int):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return dict(user)


@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    conn = get_db_connection()
    result = conn.execute(
        "UPDATE users SET name = ?, email = ? WHERE id = ?",
        (user.name, user.email, user_id),
    )
    conn.commit()
    conn.close()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated successfully"}


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    conn = get_db_connection()
    result = conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
