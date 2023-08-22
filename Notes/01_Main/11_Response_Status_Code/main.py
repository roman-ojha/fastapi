from fastapi import FastAPI, status
import uvicorn

app = FastAPI()
PORT = 8080


# The same way you can specify a response model, you can also declare the HTTP status code used for the response with the parameter 'status_code' in any of the path operations
@app.post("/items/", status_code=201)
# 'status_code' can alternatively also receive an 'IntEnum', such as Python's 'http.HTTPStatus'(https://docs.python.org/3/library/http.html#http.HTTPStatus)
async def create_item(name: str):
    # It will Return that status code in the response.
    # Also it will Document it as such in the OpenAPI schema (and so, in the user interfaces):
    return {"name": name}


@app.post("/items2/", status_code=status.HTTP_201_CREATED)
# You could also use from starlette import status.
# FastAPI provides the same starlette.status as fastapi.status just as a convenience for you, the developer. But it comes directly from Starlette.
async def create_item(name: str):
    return {"name": name}

if __name__ == "__main__":
    uvicorn.run("main:app", port=PORT, reload=True)
