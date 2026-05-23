# from fastapi, import the FastAPI class - this gives functionality to your API
from fastapi import FastAPI

# this calls FastAPI to create an instance which will become the variable 'app'
app = FastAPI()

# PATH OPERATION DECORATOR
# a 'decorator' - this tells FastAPI the function below this decorator is in charge of handling requests
# that go to:
# - the path "/"
# - using a 'get' operation (the HTTP 'GET' method which is used to READ data)
@app.get("/")

# PATH OPERATION FUNCTION
# the path is "/", the operation is 'get', and the function is below the 'decorator' (@app.get("/"))
def root():
    # returns the values, in this case a dict
    return {"message": "Hello, world!"}

###

# the value of the path parameter 'item_id' will be passed to the read_item function as item_id
@app.get("/items/{item_id}")
# therefore opening [the server ip]/items/foo will give a request to this API to run read_item and return
# {"item_id": "foo"}
def read_item(item_id):
    # in this case, "item_id": is returned with 'item_id' as the variable
    return {"item_id": item_id}

###

@app.get("/other_items/{other_item_id}")
# in this case we have declared 'other_item_id' to be an 'int'
def read_other_item(other_item_id: int):
    return {"other_item_id": other_item_id} 

###

@app.get("/users/me")
def read_user_me():
    return {"user_id": "the current user"}
# the path order here matters, if it was /users/{user_id} ABOVE /users/me, then an input of /users/me in the
# URL would never reach the 'read_user_me' function, as 'me' would be just be subbed into the variable {user_id}
@app.get("/users/{user_id}") 
def read_user(user_id: str):
    return {"user_id": user_id}