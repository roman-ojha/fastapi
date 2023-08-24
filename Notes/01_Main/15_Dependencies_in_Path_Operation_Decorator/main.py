from fastapi import FastAPI, Header, HTTPException, Depends
import uvicorn
from typing import Annotated

app = FastAPI()
PORT = 8080

# Docs: https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/#dependencies-in-path-operation-decorators


# In some cases you don't really need the return value of a dependency inside your path operation function.
# Or the dependency doesn't return a value.
# But you still need it to be executed/solved.
# For those cases, instead of declaring a path operation function parameter with 'Depends', you can add a 'list' of dependencies to the path operation decorator.


async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        # These dependencies can raise exceptions, the same as normal dependencies:
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key
    # They can return values or not, the values won't be used.
    # So, you can re-use a normal dependency (that returns a value) you already use somewhere else, and even though the value won't be used, the dependency will be executed:


@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
# These dependencies will be executed/solved the same way normal dependencies. But their value (if they return any) won't be passed to your path operation function.
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]


# In this example we use invented custom headers X-Key and X-Token.
# But in real cases, when implementing security, you would get more benefits from using the integrated Security utilities (the next chapter) (https://fastapi.tiangolo.com/tutorial/security/).


if __name__ == "__main__":
    uvicorn.run("main:app", port=PORT, reload=True)
