from fastapi import FastAPI, Query
from typing import Annotated

app = FastAPI()


@app.get("/items/")
async def read_items(q: str | None = None):
    # The query parameter q is of type Union[str, None] (or str | None in Python 3.10), that means that it's of type str but could also be None, and indeed, the default value is None, so FastAPI will know it's not required.
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Additional Validation:
# We are going to enforce that even though q is optional, whenever it is provided, its length doesn't exceed 50 characters.
# Query from fastapi
# Annotated from typing (or from typing_extensions in Python below 3.9)


@app.get("/items2/")
async def read_items(q: Annotated[str | None, Query(max_length=20, min_length=5)] = None):
    # Annotated can be used to add metadata to your parameters: https://fastapi.tiangolo.com/python-types/#type-hints-with-metadata-annotations
    # After adding Query:
    #   -> Validate the data making sure that the max length is 20 characters
    #   -> Show a clear error for the client when the data is not valid
    #   -> Document the parameter in the OpenAPI schema path operation (so it will show up in the automatic docs UI)
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Old Query as default value: https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#alternative-old-query-as-the-default-value

# Query as the default or in Annotated:
# Have in mind that when using Query inside of Annotated you cannot use the default parameter for Query.
# Have in mind that when using Query inside of Annotated you cannot use the default parameter for Query.
# For example, this is not allowed:
# q: Annotated[str, Query(default="rick")] = "morty"

# Advantage of Annotated: https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#advantages-of-annotated

# Non-Annotated:


@app.get("/items3/")
async def read_items(q: str | None = Query(default=None, min_length=5, max_length=20)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Add Regular Expression
@app.get("/items4/")
async def read_items(
    q: Annotated[
        str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$")
    ] = None
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# So, when you need to declare a value as required while using Query, you can simply not declare a default value

# Pydantic v1 'regex' instead of 'pattern': https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#pydantic-v1-regex-instead-of-pattern


# Required with Ellipsis (...)
# So, when you need to declare a value as required while using Query, you can simply not declare a default value:
@app.get("/items5/")
async def read_items(q: Annotated[str, Query(min_length=3, max_length=20)] = ...):
    # If you hadn't seen that ... before: it is a special single value, it is part of Python and is called "Ellipsis" (https://docs.python.org/3/library/constants.html#Ellipsis).
    # It is used by Pydantic and FastAPI to explicitly declare that a value is required.
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
