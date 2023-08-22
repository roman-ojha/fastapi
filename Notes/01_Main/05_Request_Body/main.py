from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Docs: https://fastapi.tiangolo.com/tutorial/body/


@app.get('/')
async def index():
    return {'msg': "Hello world"}


"""
*) Request Body:
    -> To declare a request body, you use Pydantic(https://pydantic-docs.helpmanual.io/) models with all their power and benefits.
    -> To send data, you should use one of: POST (the more common), PUT, DELETE or PATCH.
    -> Sending a body with a GET request has an undefined behavior in the specifications, nevertheless, it is supported by FastAPI, only for very complex/extreme use cases.
    -> As it is discouraged, the interactive docs with Swagger UI won't show the documentation for the body when using GET, and proxies in the middle might not support it.
"""


# Define Request Body from Pydantic's
class Item(BaseModel):
    # <name>: <type> = <default_value>
    name: str
    description: str | None = None
    # as description and tax are optional (with a default value of None)
    price: float
    tax: float | None = None


@app.post("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: str | None = None):
    # To add it to your path operation, declare it the same way you declared path and query parameters, and declare its type as the model you created, Item
    # The same as when declaring query parameters, when a model attribute has a default value, it is not required. Otherwise, it is required. Use None to make it just optional.
    print(item.name)
    print(item.description)
    print(item.price)
    return item
"""
With just that Python type declaration, FastAPI will:
    -> Read the body of the request as JSON.
    -> Convert the corresponding types (if needed).
    -> Validate the data.
    -> If the data is invalid, it will return a nice and clear error, indicating exactly where and what was the incorrect data.
    -> Give you the received data in the parameter item.
    -> As you declared it in the function to be of type Item, you will also have all the editor support (completion, etc) for all of the attributes and their types.
    -> Generate JSON Schema definitions for your model, you can also use them anywhere else you like if it makes sense for your project.
    -> Those schemas will be part of the generated OpenAPI schema, and used by the automatic documentation UIs.
"""

# Request body + path + query parameters


@app.put("/item/{item_id}")
async def create_item(item_id: int, item: Item, q: str | None = None):
    # The function parameters will be recognized as follows:
    # -> If the parameter is also declared in the path, it will be used as a path parameter.
    # -> If the parameter is of a singular type (like int, float, str, bool, etc) it will be interpreted as a query parameter.
    # -> If the parameter is declared to be of the type of a Pydantic model, it will be interpreted as a request body
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result
