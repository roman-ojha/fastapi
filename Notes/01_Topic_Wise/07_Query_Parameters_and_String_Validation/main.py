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


# Required With None
# You can declare that a parameter can accept None, but that it's still required. This would force clients to send a value, even if the value is None.
# To do that, you can declare that None is a valid type but still use ... as the default
@app.get("/items6/")
async def read_items(q: Annotated[str | None, Query(min_length=3)] = ...):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# NOTE: Pydantic, which is what powers all the data validation and serialization in FastAPI, has a special behavior when you use Optional or Union[Something, None] without a default value, you can read more about it in the Pydantic docs about Required Optional fields (https://pydantic-docs.helpmanual.io/usage/models/#required-optional-fields).


# Use Pydantic's Required instead of Ellipsis (...)
# https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#use-pydantics-required-instead-of-ellipsis


# Query parameter list / multiple values:
# When you define a query parameter explicitly with Query you can also declare it to receive a list of values, or said in other way, to receive multiple values.
@app.get("/items7/")
async def read_items(q: Annotated[list[str], Query()] = None):
    # To declare a query parameter with a type of list, like in the example above, you need to explicitly use 'Query', otherwise it would be interpreted as a request body.
    # http://127.0.0.1:8000/items7/?q=roman&q=razz
    query_items = {"q": q}
    return query_items


# Query parameter list / multiple values with defaults
@app.get("/items8/")
async def read_items(q: Annotated[list[str], Query()] = ["foo", "bar"]):
    # http://127.0.0.1:8000/items8/
    # Response:
    # {
    #   "q": [
    #     "foo",
    #     "bar"
    #   ]
    # }
    query_items = {"q": q}
    return query_items


# Using 'list'
# You can also use 'list' directly instead of List[str] (or list[str] in Python 3.9+):
@app.get("/items9/")
async def read_items(q: Annotated[list, Query()] = [1, 2, 3]):
    # Have in mind that in this case, FastAPI won't check the contents of the list.
    # For example, List[int] would check (and document) that the contents of the list are integers. But list alone wouldn't.
    query_items = {"q": q}
    return query_items


# Declare more metadata
# You can add more information about the parameter.
# That information will be included in the generated OpenAPI and used by the documentation user interfaces and external tools.

# Add 'title', 'description'
@app.get("/items10/")
async def read_items(
    q: Annotated[
        str | None,
        Query(
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
        ),
    ] = None
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Alias parameters:
# Imagine that you want the parameter to be item-query.
# Like in:
# http://127.0.0.1:8000/items/?item-query=foobaritems
# But item-query is not a valid Python variable name.
# The closest would be item_query.
# But you still need it to be exactly item-query...
# Then you can declare an alias, and that alias is what will be used to find the parameter value:


@app.get("/items11/")
async def read_items(q: Annotated[str | None, Query(alias="item-query")] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Deprecating parameters:
# Now let's say you don't like this parameter anymore.
# You have to leave it there a while because there are clients using it, but you want the docs to clearly show it as deprecated.
# Then pass the parameter deprecated=True to Query:

@app.get("/items12/")
async def read_items(
    q: Annotated[
        str | None,
        Query(
            alias="item-query",
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
            max_length=50,
            pattern="^fixedquery$",
            deprecated=True,
        ),
    ] = None
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Exclude from OpenAPI
# To exclude a query parameter from the generated OpenAPI schema (and thus, from the automatic documentation systems), set the parameter include_in_schema of Query to False:
@app.get("/items13/")
async def read_items(
    hidden_query: Annotated[str | None, Query(include_in_schema=False)] = None
):
    if hidden_query:
        return {"hidden_query": hidden_query}
    else:
        return {"hidden_query": "Not found"}
