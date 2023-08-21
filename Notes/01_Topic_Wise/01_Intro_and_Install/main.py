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
-> The command uvicorn main:app refers to:
    -> main: the file main.py (the Python "module").
    -> app: the instance object created inside of main.py with the line app = FastAPI().
    --reload: make the server restart after code changes. Only use for development.
"""


# Get Method
@app.get('/')  # <app_instance>.<operation>('<path>')
# Function in which we are defining the 'get' operation and a path using 'app' decorator is called as path operation function
# @: path operation decorator
async def index():  # Name of the function doesn't matter
    return {"msg": "Hello World"}
