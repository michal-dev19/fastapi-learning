from fastapi import FastAPI

app = FastAPI()

# we create a database (list) of 'fake items' consisting of a series of dicts, which include an "item_name"
# and random names
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# here we use a decorator which tells the API that the function below is in charge of handling requests that
# go to path "/items/" which use an operation of 'get'
@app.get("/items/")
def read_item(skip: int = 0, limit: int = 10): 
    ## declaring function parameters that aren't part of the path parameters, they are automatically 
    ## interpreted as 'query' parameters 
    return fake_items_db[skip : skip + limit]


# the query is the set of key-value pairs that go after the '?' in a URL, seperated by '&' character
# e.g in the URL: http://127.0.0.1:8000/items/?skip=0&limit=10
# the query parameters are - 'skip': with a value of 0,
                           # 'limit': with a value of 10

###

@app.get("/items/{item_id}")
# in this case we have 'item_id' which is specified in the path, but also 'q' which is not specified
# therefore 'q' is optional, and will be set to None by default
def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

###

@app.get("/items/{other_id}")
# here we also have a 'short' optional variable of type 'bool' which is by default assigned False
def read_other(other_id: str, q: str | None = None, short: bool = False):
    # if we then go to our servers URL + /items/foo?short=1 or =True or =true or =yes, the function parameter
    # 'short' will have a bool value of True, otherwise as False (default)
    other = {"other_id": other_id}
    if q:
        other.update({"q": q})
    if not short:
        other.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return other

###

@app.get("/users/{user_id}/items/{item_id}")
def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
): # in this case FastAPI will also recognise multiple variables both required in the path, and optional
    # not within the path ('q', and 'short')
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

###

@app.get("/things/{thing_id}")
def read_user_thing(thing_id: str, needy: str):
    # here the query parameter 'needy' is a required parameter of type string
    thing = {"thing_id": thing_id, "needy": needy}
    return thing

# therefore if we open URL http://127.0.0.1:8000/items/foo-item, WITHOUT adding the required parameter 'needy',
# we will see an error
# obviously to avoid this error, we set the required parameter like so:
# http://127.0.0.1:8000/items/foo-item?needy=sooooneedy