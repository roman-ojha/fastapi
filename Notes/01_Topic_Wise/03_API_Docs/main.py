from typing import Union
from fastapi import FastAPI

app = FastAPI()

# Default Swagger Api documentation route: http://127.0.0.1:<port>/docs
# Alternative API Docs from 'ReDoc': http://127.0.0.1:8000/redoc
# Json Schema: http://127.0.0.1:8000/openapi.json

# OpenAPI: https://fastapi.tiangolo.com/tutorial/first-steps/#openapi


@app.get('/')
async def index():
    return {"msg": "Hello World"}


@app.get('/item/{item_id}')
async def index(item_id):
    return {"item_id": item_id}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
