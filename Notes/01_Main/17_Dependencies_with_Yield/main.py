from fastapi import FastAPI, Depends
import uvicorn
from typing import Annotated

app = FastAPI()
PORT = 8080

# Docs: https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/

# FastAPI supports dependencies that do some extra steps after finishing.
# To do this, use 'yield' instead of 'return', and write the extra steps after.


# A Database dependency with yield:
# For example, you could use this to create a database session and close it after finishing.
# Only the code prior to and including the 'yield' statement is executed before sending a response

class DBSession:
    # Database Configuration
    pass


# You can use async or normal functions.
# FastAPI will do the right thing with each, the same as with normal dependencies.
async def get_db():
    db = DBSession()
    # If you use a 'try' block in a dependency with 'yield', you'll receive any exception that was thrown when using the dependency.
    # So, you can look for that specific exception inside the dependency with 'except <SomeException>'.
    try:
        yield db
        # The yielded value is what is injected into path operations and other dependencies
    # The code following the yield statement is executed after the response has been delivered
    finally:
        # In the same way, you can use finally to make sure the exit steps are executed, no matter if there was an exception or not.
        db.close()


# Sub-dependencies with yield:
# You can have sub-dependencies and "trees" of sub-dependencies of any size and shape, and any or all of them can use yield.
# FastAPI will make sure that the "exit code" in each dependency with yield is run in the correct order.
# For example, 'dependency_c' can have a dependency on 'dependency_b', and 'dependency_b' on 'dependency_a' And all of them can use 'yield'
class DepA:
    def close(self):
        print("Closing Dependency A")


class DepB:
    def close(self, dep: DepA):
        print("Closing Dependency B")


class DepC:
    def close(self, dep: DepB):
        print("Closing Dependency C")


async def generate_dep_a():
    return DepA()


async def generate_dep_b():
    return DepB()


async def generate_dep_c():
    return DepC()


async def dependency_a():
    dep_a = generate_dep_a()
    try:
        print("Opening Dependency A")
        yield dep_a
        # The same way, you could have dependencies with 'yield' and 'return' mixed.
    finally:
        dep_a.close()


async def dependency_b(dep_a: Annotated[DepA, Depends(dependency_a)]):
    dep_b = generate_dep_b()
    try:
        print("Opening Dependency B")
        yield dep_b
    finally:
        dep_b.close(dep_a)


async def dependency_c(dep_b: Annotated[DepB, Depends(dependency_b)]):
    dep_c = generate_dep_c()
    try:
        print("Opening Dependency C")
        yield dep_c
    finally:
        dep_c.close(dep_b)


@app.get('/')
async def index(dep_c: Annotated[DepC, Depends(dependency_c)]):
    return {}


# In this case dependency_c, to execute its exit code, needs the value from dependency_b (here named dep_b) to still be available.
# And, in turn, dependency_b needs the value from dependency_a (here named dep_a) to be available for its exit code.
# FastAPI will make sure everything is run in the correct order.
# This works thanks to Python's Context Managers(https://docs.python.org/3/library/contextlib.html).
# FastAPI uses them internally to achieve this.

# NOTE: You can still raise exceptions including HTTPException before the yield. But not after.
# Docs on Dependencies with 'yield' & 'HTTPException': https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/#dependencies-with-yield-and-httpexception


# Context Manager: https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/#context-managers


if __name__ == "__main__":
    uvicorn.run("main:app", port=PORT, reload=True)
