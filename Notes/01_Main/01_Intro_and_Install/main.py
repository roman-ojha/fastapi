"""
-> Install: https://fastapi.tiangolo.com/#installation
-> Uses Uvicorn or Hypercorn ASGI Server:
    -> https://www.uvicorn.org/
    -> https://github.com/pgjones/hypercorn

"""


from typing import Union
from fastapi import FastAPI

# FastAPI is a Python class that provides all the functionality for your API.
app = FastAPI()

# FastAPI is a class that inherits directly from Starlette.

# You can use all the Starlette(https://www.starlette.io/) functionality with FastAPI too.
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
    # Return The Content:
    # You can return a dict, list, singular values as str, int, etc.
    # You can also return Pydantic models (you'll see more about that later).
    # There are many other objects and models that will be automatically converted to JSON (including ORMs, etc). Try using your favorite ones, it's highly probable that they are already supported.
    return {"msg": "Hello World"}

# You can define 'async' and normal function, difference: https://fastapi.tiangolo.com/async/#in-a-hurry

"""
You can also use the other operations:
    -> @app.post()
    -> @app.put()
    -> @app.delete()
And the more exotic ones:
    -> @app.options()
    -> @app.head()
    -> @app.patch()
    -> @app.trace()
"""
