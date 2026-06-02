from fastapi import FastAPI, Depends, HTTPException, status, Header
import bcrypt
from jose import jwt, JWTError
from pydantic import BaseModel
from datetime import datetime, timedelta
import sqlite3


app = FastAPI()


class UserCreate(BaseModel):
    email: str
    password: str


SECRET_KEY = "BHOS83j0SnjaF2004o"
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def create_token(id: str) -> str:
    return jwt.encode(
        {"sub": id, "exp": datetime.utcnow() + timedelta(seconds=60000)},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def init_db():
    # establish a connection with the DB and connect it to the cursor
    # (we do this internally because this is a server, handling multiple requests at a time)
    conn = sqlite3.connect("auth.db")
    cursor = conn.cursor()

    # populate the database with 'users' if not done so already
    try:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT, password TEXT)"
        )
        conn.commit()
    except sqlite3.Error:
        raise HTTPException(status_code=500, detail="Internal server error")


# initialises DB on app startup
@app.on_event("startup")
def startup():
    init_db()


# runs a registration operation to validate store user data in 'users'
@app.post("/register")
def register_user(user_info: UserCreate):
    # establish connection with the DB
    conn = sqlite3.connect("auth.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (user_info.email, hash_password(user_info.password)),
        )
        conn.commit()
    except sqlite3.Error:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

    return {"Success": "true"}


# recieves data from the user to log them in, function validates and verifies user input
@app.post("/login")
def login_user(user_info: UserCreate):
    conn = sqlite3.connect("auth.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id, email, password FROM users WHERE email=?", (user_info.email,)
        )
    except sqlite3.Error:
        raise HTTPException(status_code=500, detail="Internal server error")

    info_list = cursor.fetchone()
    if info_list is None:
        raise HTTPException(status_code=404, detail="Item not found")

    if bcrypt.checkpw(user_info.password.encode("utf-8"), info_list[2].encode("utf-8")):
        return create_token(str(info_list[0]))
    return {"Success": "false"}


# authorises the user with their signed token
def get_current_user(authorization: str = Header(None)):
    print(authorization)
    if authorization is None:
        raise HTTPException(status_code=401, detail="Unauthorised")
    encoded_token = authorization.split(" ")[1]
    try:
        return jwt.decode(token=encoded_token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as e:
        print(f"JWT Error: {e}")
        raise HTTPException(status_code=401, detail="Unauthorised")


# completes authorisation for desired path for the user
@app.get("/me")
def read_me(current_user=Depends(get_current_user)):
    return current_user
