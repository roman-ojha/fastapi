from typing import Union
from fastapi import FastAPI
from enum import Enum

app = FastAPI()

# https://fastapi.tiangolo.com/tutorial/path-params/


@app.get('/')
async def index():
    return {"msg": "Hello World"}


@app.get('/item/{item_id}')
async def index(item_id):
    return {"item_id": item_id}


# http://127.0.0.1:8000/items/5?q=roman
@app.get("/items/{item_id}")
# The value of the path parameter 'item_id' will be passed to your function as the argument 'item_id'.
async def read_item(item_id: int, q: Union[str, None] = None):
    # Notice that the value your function received (and returned) is 5, as a Python int, not a string "5".
    # So, with that type declaration, FastAPI gives you automatic request "parsing".
    # Pydantic: https://fastapi.tiangolo.com/tutorial/path-params/#pydantic
    return {"item_id": item_id, "q": q}


# @app.get("/items/{item_id}")
# async def read_item(item_id: str):
#     return {"item_id": item_id}

"""
*) Order matters
    -> When creating path operations, you can find situations where you have a fixed path.
    -> Like /users/me, let's say that it's to get data about the current user.
    -> And then you can also have a path /users/{user_id} to get data about a specific user by some user ID.
    -> Because path operations are evaluated in order, you need to make sure that the path for /users/me is declared before the one for /users/{user_id}:
    -> you cannot redefine a path operation, The first one will always be used since the path matches first
"""


# Predefined Values:
# If you have a path operation that receives a path parameter, but you want the possible valid path parameter values to be predefined, you can use a standard Python 'Enum'.
class UserName(str, Enum):
    roman = "roman"
    razz = "razz"


@app.get('/user/{username}')
async def get_user(username: UserName):
    if username is UserName.roman:
        return {'username': username, 'msg': "Hello Roman"}
    if username.value == 'razz':
        # You can get the actual value (a str in this case) using username.value, or in general, your_enum_member.value:
        # You could also access the value "razz" with UserName.razz.value.
        return {'username': username, 'msg': "Hello Razz"}
        # You can return enum members from your path operation, even nested in a JSON body (e.g. a dict).
        # They will be converted to their corresponding values (strings in this case) before returning them to the client


"""
*) Path parameters containing paths:
    -> Let's say you have a path operation with a path /files/{file_path}.
    -> But you need file_path itself to contain a path, like home/johndoe/myfile.txt.
    -> So, the URL for that file would be something like: /files/home/johndoe/myfile.txt
    *) OpenAPI support
        -> OpenAPI doesn't support a way to declare a path parameter to contain a path inside, as that could lead to scenarios that are difficult to test and define.
        -> Nevertheless, you can still do it in FastAPI, using one of the internal tools from Starlette.
        -> And the docs would still work, although not adding any documentation telling that the parameter should contain a path.
    
    -> Using an option directly from Starlette you can declare a path parameter containing a path using a URL like:
        -> /files/{file_path:path}
    -> In this case, the name of the parameter is file_path, and the last part, :path, tells it that the parameter should match any path.
"""


@app.get('/files/{file_path:path}')
async def read_file(file_path: str):
    return {"file_path": file_path}

# You could need the parameter to contain /home/johndoe/myfile.txt, with a leading slash (/).
# In that case, the URL would be: /files//home/johndoe/myfile.txt, with a double slash (//) between files and home
