from typing import Union
from fastapi import FastAPI

app = FastAPI()


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
    return {"item_id": item_id, "q": q}


# @app.get("/items/{item_id}")
# async def read_item(item_id: str):
#     return {"item_id": item_id}
