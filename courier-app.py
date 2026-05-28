import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

conn = sqlite3.connect("courier.db", check_same_thread=False)
cursor = conn.cursor()

app = FastAPI()


class Driver(BaseModel):
    name: str
    email: str


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


# this operation returns all the individual drivers' information within 'users' table
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


# this operation returns specified driver information within 'users' table
@app.get("/drivers/{id}")
def get_user(id: int):
    cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
    user_info = cursor.fetchone()
    if user_info is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"driver": {"id": user_info[0], "name": user_info[1], "email": user_info[2]}}


# delete a user from the 'users' table
@app.delete("/drivers/{id}")
def delete_user(id: int):
    cursor.execute("DELETE FROM users WHERE id = ?", (id,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"deletion": "Success"}


# recieve incoming POST data into API
@app.post("/drivers")
def create_user(new_driver: Driver):
    # try except block to catch errors
    try:
        # insert new data into database
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (new_driver.name, new_driver.email),
        )
        conn.commit()
    except sqlite3.Error:
        raise HTTPException(status_code=500, detail="Internal server error")
    return {"new_driver": {"name": new_driver.name, "email": new_driver.email}}


# update existing data within database
@app.put("/drivers/{id}")
def update_user(updated_driver: Driver, id: int):
    # try except block for catching errors
    try:
        # updates specific data for given id
        cursor.execute(
            "UPDATE users SET name=?, email=? WHERE id=?",
            (updated_driver.name, updated_driver.email, id),
        )
        # if no changes were made, raise error
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        conn.commit()
    except sqlite3.Error:
        raise HTTPException(status_code=500, detail="Internal server error")
    return {
        "updated_driver": {"name": updated_driver.name, "email": updated_driver.email}
    }


if __name__ == "__main__":
    uvicorn.run("courier-app:app", reload=True)
