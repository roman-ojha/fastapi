from fastapi import FastAPI, Depends
import uvicorn
from typing import Annotated


app = FastAPI()
PORT = 8080


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

# The key factor is that a dependency should be a "callable".
# A "callable" in Python is anything that Python can "call" like a function.
# Then, in FastAPI, you could use a Python class as a dependency.
# What FastAPI actually checks is that it is a "callable" (function, class or anything else) and the parameters defined.

fake_items_db = [{"item_name": "Foo"}, {
    "item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:
    def __init__(self, q: str | None, skip: int = 0, limit: int = 100) -> None:
        # Pay attention to the __init__ method used to create the instance of the class:
        # it has the same parameters as our previous 'common_parameters'
        # In both cases the data will be converted, validated, documented on the OpenAPI schema, etc.
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get('/items/')
async def read_items(commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]):
    # the first 'CommonQueryParams' in Annotated doesn't have any special meaning for FastAPI. FastAPI won't use it for data conversion, validation, etc. (as it is using the Depends(CommonQueryParams) for that).
    # But you see that we are having some code repetition here, writing CommonQueryParams twice
    # FastAPI provides a shortcut for these cases, in where the dependency is specifically a class that FastAPI will "call" to create an instance of the class itself.
    response = {}
    if commons.q:
        # now here we can see that we will get the IDE intelligence support
        response.update({'q': commons.q})
    items = fake_items_db[commons.skip:commons.skip + commons.limit]
    response.update({"items": items})
    return response


@app.get("/items/")
async def read_items(commons: Annotated[CommonQueryParams, Depends()]):
    # You declare the dependency as the type of the parameter, and you use Depends() without any parameter, instead of having to write the full class again inside of Depends(CommonQueryParams) and FastAPI will know what to do.
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip: commons.skip + commons.limit]
    response.update({"items": items})
    return response

if __name__ == "__main__":
    uvicorn.run("main:app", port=PORT, reload=True)
