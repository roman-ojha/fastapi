from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel, EmailStr
from typing import Any

app = FastAPI()
PORT = 8080

# Docs: https://fastapi.tiangolo.com/tutorial/response-model/


@app.get('/')
async def index():
    return "Hello World"


# You can declare the type used for the response by annotating the path operation function return type.
# You can use type annotations the same way you would for input data in function parameters, you can use Pydantic models, lists, dictionaries, scalar values like integers, booleans, etc.

# Defining Model which we will use on Parameter & return type

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


@app.post('/items/')
async def create_item(item: Item) -> Item:
    return item


@app.get('/items/')
async def read_item() -> list[Item]:
    # FastAPI will use this return type to:
    #   -> Validate the returned data.
    #       -> If the data is invalid (e.g. you are missing a field), it means that your app code is broken, not returning what it should, and it will return a server error instead of returning incorrect data. This way you and your clients can be certain that they will receive the data and the data shape expected.
    #   -> Add a JSON Schema for the response, in the OpenAPI path operation.
    #       -> This will be used by the automatic docs.
    #       -> It will also be used by automatic client code generation tools.
    #   -> But most importantly:
    #       -> It will limit and filter the output data to what is defined in the return type.
    #       -> This is particularly important for security, we'll see more of that below.
    return [
        Item(name="Portal Gun", price=43.1),
        Item(name="Plumbus", price=64.2),
    ]


# 'response_model' Parameter:
# There are some cases where you need or want to return some data that is not exactly what the type declares.
# For example, you could want to return a dictionary or a database object, but declare it as a Pydantic model. This way the Pydantic model would do all the data documentation, validation, etc. for the object that you returned (e.g. a dictionary or database object).
# If you added the return type annotation, tools and editors would complain with a (correct) error telling you that your function is returning a type (e.g. a dict) that is different from what you declared (e.g. a Pydantic model).
# In those cases, you can use the path operation decorator parameter 'response_model' instead of the return type.
# You can use the response_model parameter in any of the path operations, 'get', 'post', 'put', 'delete' etc ...

@app.get('/items2/', response_model=list[Item])
# 'response_model' receives the same type you would declare for a Pydantic model field, so, it can be a Pydantic model, but it can also be, e.g. a 'list' of Pydantic models, like 'List[Item]'.
# FastAPI will use this 'response_model' to do all the data documentation, validation, etc. and also to convert and filter the output data to its type declaration.
async def read_items() -> any:
    # If you have strict type checks in your editor, mypy, etc, you can declare the function return type as 'Any'.
    # That way you tell the editor that you are intentionally returning anything. But FastAPI will still do the data documentation, validation, filtering, etc. with the 'response_model'.
    return [
        Item(name="Portal Gun", price=43.1),
        Item(name="Plumbus", price=64.2),
    ]


"""
*) 'response_model' Priority:
    -> If you declare both a return type and a 'response_model', the 'response_model' will take priority and be used by FastAPI.
    -> This way you can add correct type annotations to your functions even when you are returning a type different than the response model, to be used by the editor and tools like mypy. And still you can have FastAPI do the data validation, documentation, etc. using the 'response_model'.
    -> You can also use response_model=None to disable creating a response model for that path operation, you might need to do it if you are adding type annotations for things that are not valid Pydantic fields, you will see an example of that in one of the sections below.

"""


# Return the same input data:
class User(BaseModel):
    # And we are using this model to declare our input and the same model to declare our output
    username: str
    # Now, whenever a browser is creating a user with a password, the API will return the same password in the response.
    # In this case, it might not be a problem, because it's the same user sending the password.
    # But if we use the same model for another path operation, we could be sending our user's passwords to every client.
    password: str
    email: EmailStr  # pip install pydantic[email]
    full_name: str | None = None


# We can instead create an input model with the plaintext password and an output model without it
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    # Here, even though our path operation function is returning the same input user that contains the password we declared the response_model to be our model UserOut, that doesn't include the password
    # So, FastAPI will take care of filtering out all the data that is not declared in the output model (using Pydantic).
    return user


# 'response_model' or Return Type:
# In this case, because the two models are different, if we annotated the function return type as UserOut, the editor and tools would complain that we are returning an invalid type, as those are different classes.
# That's why in this example we have to declare it in the response_model parameter.
# ...but continue reading below to see how to overcome that


"""
*) 
"""


if __name__ == "__main__":
    uvicorn.run("main:app", port=PORT, reload=True)
