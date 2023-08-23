from fastapi import FastAPI, Depends
import uvicorn
from typing import Annotated

app = FastAPI()
PORT = 8080

# Docs: https://fastapi.tiangolo.com/tutorial/dependencies/#dependencies

# What is "Dependency Injection": https://fastapi.tiangolo.com/tutorial/dependencies/#what-is-dependency-injection

# Example:
# Creating Dependency


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    # this is the dependency function which we use bellow
    # here all the function parameter that we are getting needs to come through some Parameter which user try to request to the path endpoint, we can see that in api documentation as well
    return {"q": q, "skip": skip, "limit": limit}


# The same way you use Body, Query, etc. with your path operation function parameters, use Depends with a new parameter:
@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    # Although you use 'Depends' in the parameters of your function the same way you use 'Body', 'Query', etc, 'Depends' works a bit differently.
    # You only give 'Depends' a single parameter.
    """
    *) Whenever a new request arrives, FastAPI will take care of:
        -> Calling your dependency ("dependable") function with the correct parameters.
        -> Get the result from your function.
        -> Assign that result to the parameter in your path operation function.
    """
    return commons


@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


# In the examples above, you see that there's a tiny bit of code duplication.
# When you need to use the common_parameters() dependency, you have to write the whole parameter with the type annotation and Depends():
# commons: Annotated[dict, Depends(common_parameters)]
# But because we are using Annotated, we can store that Annotated value in a variable and use it in multiple places:

CommonsDep = Annotated[dict, Depends(common_parameters)]
# This is just standard Python, it's called a "type alias", it's actually not specific to FastAPI.


"""
*) The simplicity of the dependency injection system makes FastAPI compatible with:
    -> all the relational databases
    -> NoSQL databases
    -> external packages
    -> external APIs
    -> authentication and authorization systems
    -> API usage monitoring systems
    -> response data injection systems
    -> etc ...
"""

# You can define dependencies that in turn can define dependencies themselves.
# In the end, a hierarchical tree of dependencies is built, and the Dependency Injection system takes care of solving all these dependencies for you (and their sub-dependencies) and providing (injecting) the results at each step.
# Dependency injection system hierarchy: https://fastapi.tiangolo.com/tutorial/dependencies/#simple-and-powerful


@app.get("/users2/")
async def read_users(commons: CommonsDep):
    return commons

if __name__ == "__main__":
    uvicorn.run("main:app", port=PORT, reload=True)
