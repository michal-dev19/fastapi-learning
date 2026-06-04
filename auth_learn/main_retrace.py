import sqlite3
from jose import jwt, JWTError
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
import bcrypt
from datetime import datetime, timedelta

app = FastAPI()

SECRET_KEY = "JS3ON3OS90G0V82J"
ALGORITHM = "HS256"


# this function calls the user's original password, adds a 'salt', hashes it and returns the value
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


# this function creates a specialised, signed token for the user
def create_token(user_info: str) -> list:
    return jwt.encode(
        {"sub": user_info[0], "exp": (datetime.utcnow() + timedelta(hours=1))},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


# this function authorises the current user by checking signed token
def get_current_user(authorization: str = Header()):
    try:
        return jwt.decode(authorization, SECRET_KEY, algorithms=ALGORITHM)
    except JWTError:
        raise HTTPException(status_code=401, detail="Unauthorized")


# a class with inheritance from Header for handling JSON posts from user to server
class CreateUser(BaseModel):
    email: str
    password: str


###this file functions to run inside a server, so code will be server appropriate and be able to handle large requests one-by-one###


# first I need to set up a database to store user info, initialise it and seed it
def init():
    # set up connection and cursor
    conn = sqlite3.connect("auth_retrace.db")
    cursor = conn.cursor()
    # try/except block for catching errors, this creates the users table in the DB
    try:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT, password TEXT)"
        )
        conn.commit()
    except sqlite3.Error:
        conn.rollback()
        raise RuntimeError


init()


# seeding is unnecessary in this case, so we continue on to /register
@app.post("/register")
def register_user(register_input: CreateUser):
    # connect to DB
    conn = sqlite3.connect("auth_retrace.db")
    cursor = conn.cursor()
    # here we check whether the email in the request is already present in DB, if so return 400
    try:
        cursor.execute("SELECT * FROM users WHERE email=?", (register_input.email,))
    except sqlite3.Error:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Bad Request")
    # now we insert the data into 'users'
    try:
        cursor.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (register_input.email, hash_password(register_input.password)),
        )
        conn.commit()
    except sqlite3.Error:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")


# once a user is registered, they need to be able to login
@app.post("/login")
def login_user(login_input: CreateUser):
    # we need to compare user's input to stored values in DB, if values exist
    conn = sqlite3.connect("auth_retrace.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id, email, password FROM users WHERE email=?", (login_input.email,)
        )
    except sqlite3.Error:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    # we store the user's info in a list we can later access
    user_info = cursor.fetchone()
    print(user_info)
    if not user_info:
        raise HTTPException(status_code=404, detail="Item Not Found")

    # check whether inputted password matches stored hashed password
    if bcrypt.checkpw(
        login_input.password.encode("utf-8"), str(user_info[2]).encode("utf-8")
    ):
        return create_token(user_info)
    return {"Status": "Failure"}


# accessing a protected route needs authorisation, we use Depends(get_current_user) to instruct FastAPI to call 'get_current_user' when a
# request is received, this then returns the payload of the user's token into 'user', we then return this payload
@app.post("/me")
def me(user=Depends(get_current_user)):
    return user
