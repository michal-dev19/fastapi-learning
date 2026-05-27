import sqlite3
from fastapi import FastAPI
import uvicorn

conn = sqlite3.connect("courier.db", check_same_thread=False)
cursor = conn.cursor()

app = FastAPI()


def init_db():
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY, driver_id INT, destination TEXT)"
    )
    conn.commit()


init_db()


def seed_db():
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.execute(
            "INSERT INTO users (name, email) VALUES ('Jim', 'jim@email.com'), ('Jeff', 'jeff@gmail.com')"
        )
        conn.commit()

    cursor.execute("SELECT COUNT(*) FROM jobs")
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.execute(
            "INSERT INTO jobs (driver_id, destination) VALUES (1, 'Wallasey'), (2, 'Rhyll')"
        )
        conn.commit()


seed_db()


@app.get("/drivers")
def get_drivers():
    cursor.execute("SELECT * FROM users")
    # a list comprehension attaching values from a for loop to dict objects, each iteration creating a new dict
    # returns this list in a dict format of {"drivers": *list*}
    return {
        "drivers": [
            {"id": item[0], "name": item[1], "email": item[2]}
            for item in cursor.fetchall()
        ]
    }


if __name__ == "__main__":
    uvicorn.run("courier-app:app", reload=True)
