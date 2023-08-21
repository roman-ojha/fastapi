from fastapi import FastAPI

app = FastAPI()

# Docs: https://fastapi.tiangolo.com/tutorial/query-params/#query-parameters


@app.get('/')
async def index():
    return {'msg': "Hello world"}


# When you declare other function parameters that are not part of the path parameters, they are automatically interpreted as "query" parameters.
@app.get('/user')
async def get_user(username: str = "roman", id: int = 0):
    # Given default value are even available on API Docs
    return {'username': username, 'id': id}

# The query is the set of key-value pairs that go after the ? in a URL, separated by & characters.

# All the same process that applied for path parameters also applies for query parameters:
# -> Editor support (obviously)
# -> Data "parsing"
# -> Data validation
# -> Automatic documentation


# Optional Parameters:
# The same way, you can declare optional query parameters, by setting their default to None:
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    # Also notice that FastAPI is smart enough to notice that the path parameter item_id is a path parameter and q is not, so, it's a query parameter.
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


# Query Parameter with 'bool' type
@app.get("/item/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    # http://127.0.0.1:8000/items/foo?short=1
    # http://127.0.0.1:8000/items/foo?short=True
    # http://127.0.0.1:8000/items/foo?short=true
    # http://127.0.0.1:8000/items/foo?short=on
    # http://127.0.0.1:8000/items/foo?short=yes
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# Multiple path and query parameters
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# Required query parameters
# -> When you declare a default value for non-path parameters (for now, we have only seen query parameters), then it is not required.
# -> If you don't want to add a specific value but just make it optional, set the default as None.
# -> But when you want to make a query parameter required, you can just not declare any default value

# NOTE: You could also use 'Enum's the same way as with path parameter
