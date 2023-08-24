from fastapi import FastAPI, Header, Depends, HTTPException
import uvicorn
from typing import Annotated

# Docs: https://fastapi.tiangolo.com/tutorial/dependencies/global-dependencies/#global-dependencies


# For some types of applications you might want to add dependencies to the whole application.
# Similar to the way you can add dependencies to the path operation decorators, you can add them to the FastAPI application.
# In that case, they will be applied to all the path operations in the application:

async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])
PORT = 8080

if __name__ == "__main__":
    uvicorn.run("main:app", port=PORT, reload=True)
