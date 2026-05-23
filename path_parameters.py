from enum import Enum

from fastapi import FastAPI
# we import both FastAPI for functionality and Enum which is a type of fixed set of allowed values

# we can then create our own class 'ModelName', which inherits Enum to make sure the data within ModelName
# stays the same and does not change, and str makes every Enum member behave as a string so that it can 
# be serialised to JSON and displayed in the docs correctly
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

# again we create an instance within the FastAPI class and name it 'app'
app = FastAPI()

# we use a decorator with a operation of 'get' and a path of "/models/{model_name}"
@app.get("/models/{model_name}")
# the function used here takes as input 'model_name' which follows the inheritance of 'ModelName' and
# keeps to its strict types (if an input doesn't match these types, it automatically causes an error)
def get_model(model_name: ModelName):
    # finally we have conditionals to determine what message we will output based on the 'fixed' input we 
    # have recieved from the path
    # in this conditional we are comparing the enum member 'model_name' to an enum member within the ModelName
    # class 'alexnet'
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    
    # in this conditional, we can actually grab the value of the 'model_name' enum member, which is a string
    # and compare the string value
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    
    return {"model_name": model_name, "message": "Have some residuals"}