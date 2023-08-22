from fastapi import FastAPI, Response
import uvicorn
from pydantic import BaseModel, EmailStr
from typing import Any
from fastapi.responses import JSONResponse, RedirectResponse

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
*) Return Type and Data Filtering:
    -> Let's continue from the previous example. We wanted to annotate the function with one type but return something that includes more data.
    -> We want FastAPI to keep filtering the data using the response model.
    -> In the previous example, because the classes were different, we had to use the response_model parameter. But that also means that we don't get the support from the editor and tools checking the function return type.
    -> But in most of the cases where we need to do something like this, we want the model just to filter/remove some of the data as in this example.
    -> And in those cases, we can use classes and inheritance to take advantage of function type annotations to get better support in the editor and tools, and still get the FastAPI data filtering.
"""


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn2(BaseUser):
    # 'BaseUser' has the base fields. Then 'UserIn' inherits from 'BaseUser' and adds the password field, so, it will include all the fields from both models.
    password: str


@app.post("/user2/")
async def create_user(user: UserIn2) -> BaseUser:
    # We annotate the function return type as 'BaseUser', but we are actually returning a 'UserIn' instance.
    # The editor, mypy, and other tools won't complain about this because, in typing terms, 'UserIn' is a subclass of 'BaseUser', which means it's a valid type when what is expected is anything that is a 'BaseUser'.
    return user


# FastAPI Data Filtering: https://fastapi.tiangolo.com/tutorial/response-model/#fastapi-data-filtering


# Return A Response Directly:
# The most common case would be returning a Response directly as explained later in the advanced docs(https://fastapi.tiangolo.com/advanced/response-directly/)


@app.get("/portal")
async def get_portal(teleport: bool = False) -> Response:
    # This simple case is handled automatically by FastAPI because the return type annotation is the class (or a subclass) of 'Response'
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    # And tools will also be happy because both 'RedirectResponse' and 'JSONResponse' are subclasses of Response, so the type annotation is correct.
    return JSONResponse(content={"message": "Here's your interdimensional portal."})


# You can also use a subclass of Response in the type annotation
@app.get("/teleport")
async def get_teleport() -> RedirectResponse:
    # This will also work because 'RedirectResponse' is a subclass of 'Response', and FastAPI will automatically handle this simple case.
    return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")


# Invalid Return Type Annotations: https://fastapi.tiangolo.com/tutorial/response-model/#invalid-return-type-annotations


# Disable Response Model:
# Continuing from the example above, you might not want to have the default data validation, documentation, filtering, etc. that is performed by FastAPI.
# But you might want to still keep the return type annotation in the function to get the support from tools like editors and type checkers (e.g. mypy).
# In this case, you can disable the response model generation by setting response_model=None
@app.get("/portal2", response_model=None)
async def get_portal(teleport: bool = False) -> Response | dict:
    # This will make FastAPI skip the response model generation and that way you can have any return type annotations you need without it affecting your FastAPI application.
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return {"message": "Here's your interdimensional portal."}


# Use the 'response_model_exclude_unset' parameter:
# Use 'response_model_exclude_unset' to return only the values explicitly set
class Item2(BaseModel):
    name: str
    # Your response model could have default values, like:
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []
    # but you might want to omit them from the result if they were not actually stored
    # For example, if you have models with many optional attributes in a NoSQL database, but you don't want to send very long JSON responses full of default values.


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items3/{item_id}", response_model=Item2, response_model_exclude_unset=True)
# You can set the path operation decorator parameter response_model_exclude_unset=True, and those default values won't be included in the response, only the values actually set
# You can also use:
# response_model_exclude_defaults=True
# response_model_exclude_none=True
# as described in the Pydantic docs for 'exclude_defaults' and 'exclude_none'.
async def read_item(item_id: str):
    # So, if you send a request to that path operation for the item with ID foo, the response (not including default values) will be:
    # {
    #     "name": "Foo",
    #     "price": 50.2
    # }
    return items[item_id]


# 'response_model_include' and 'response_model_exclude'
# They take a 'set' of 'str' with the name of the attributes to include (omitting the rest) or to exclude (including the rest).
# This can be used as a quick shortcut if you have only one Pydantic model and want to remove some data from the output.
# But it is still recommended to use the ideas above, using multiple classes, instead of these parameters.
# This is because the JSON Schema generated in your app's OpenAPI (and the docs) will still be the one for the complete model, even if you use 'response_model_include' or 'response_model_exclude' to omit some attributes.

@app.get(
    "/items4/{item_id}/name",
    response_model=Item2,
    # response_model_include={"name", "description"},
    # The syntax {"name", "description"} creates a set with those two values.
    # It is equivalent to set(["name", "description"]).
    # Using lists instead of sets
    response_model_include=["name", "description"],
)
async def read_item_name(item_id: str):
    return items[item_id]


if __name__ == "__main__":
    uvicorn.run("main:app", port=PORT, reload=True)
