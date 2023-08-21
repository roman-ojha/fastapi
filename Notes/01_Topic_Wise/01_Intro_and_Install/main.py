
"""
-> Install: https://fastapi.tiangolo.com/#installation
-> Uses Uvicorn or Hypercorn ASGI Server:
    -> https://www.uvicorn.org/
    -> https://github.com/pgjones/hypercorn

"""


from typing import Union
from fastapi import FastAPI

app = FastAPI()
"""
=> Start Server:
    -> uvicorn main:app --reload
    -> uvicorn main:app --reload --port=8080

-> Because we are using app instance for fastapi we will use main:app to run the server
"""


@app.get('/')
async def read_root():
    return {"msg": "Hello World"}
