from fastapi import FastAPI, Depends, Cookie
import uvicorn
from typing import Annotated

app = FastAPI()
PORT = 8080

# Docs: https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/#sub-dependencies

# You can create dependencies that have sub-dependencies.
# They can be as deep as you need them to be.
# FastAPI will take care of solving them.

# First Dependency, "Dependable"


def query_extractor(q: str | None = None):
    # It declares an optional query parameter q as a str, and then it just returns it.
    return q


# Second dependency, "dependable" and "dependant"
# creating another dependency function (a "dependable") that at the same time declares a dependency of its own (so it is a "dependant" too):
def query_or_cookie_extractor(
    q: Annotated[str, Depends(query_extractor)],
    last_query: Annotated[str | None, Cookie()] = None,
):
    # Even though this function is a dependency ("dependable") itself, it also declares another dependency (it "depends" on something else).
    # It depends on the 'query_extractor', and assigns the value returned by it to the parameter 'q'.

    if not q:
        return last_query
    return q


@app.get("/items/")
async def read_query(
    query_or_default: Annotated[str, Depends(query_or_cookie_extractor)]
):
    return {"q_or_cookie": query_or_default}

# Notice that we are only declaring one dependency in the path operation function, the query_or_cookie_extractor.
# But FastAPI will know that it has to solve query_extractor first, to pass the results of that to query_or_cookie_extractor while calling it.

# 'query_extractor'
#       |
# 'query_or_cookie_extractor'
#       |
#    '/items/'

# Using the same dependency multiple times: https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/#using-the-same-dependency-multiple-times

if __name__ == "__main__":
    uvicorn.run("main:app", port=PORT, reload=True)
