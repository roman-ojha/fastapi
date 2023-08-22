from typing import Union
from fastapi import FastAPI
from enum import Enum

app = FastAPI()

# Default Swagger Api documentation route: http://127.0.0.1:<port>/docs
# Alternative API Docs from 'ReDoc': http://127.0.0.1:8000/redoc
# Json Schema: http://127.0.0.1:8000/openapi.json

# OpenAPI: https://fastapi.tiangolo.com/tutorial/first-steps/#openapi


@app.get('/')
async def index():
    return {"msg": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


class UserName(str, Enum):
    roman = "roman"
    razz = "razz"


# Path parameter Docs: Because the available values for the path parameter are predefined 'UserName' enum, the interactive docs can show them nicely:
@app.get('/user/{username}')
async def get_user(username: UserName):
    if username is UserName.roman:
        return {'username': username, 'msg': "Hello Roman"}
    if username.value == 'razz':
        return {'username': username, 'msg': "Hello Razz"}
