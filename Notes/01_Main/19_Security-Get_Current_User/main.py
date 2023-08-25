from fastapi import FastAPI, Depends
import uvicorn
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from pydantic import BaseModel

app = FastAPI()
PORT = 8080


# Create a user model
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def fake_decode_token(token):
    # Here we are returning the user if that match with the 'token' value and also return fake email with full_name
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    # get_current_user will have a dependency with the same 'oauth2_scheme' we created before
    # The same as we were doing before in the path operation directly, our new dependency 'get_current_user' will receive a 'token' as a 'str' from the sub-dependency 'oauth2_scheme'
    user = fake_decode_token(token)
    return user


@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    # So now we can use the same 'Depends' with our 'get_current_user' in the path operation
    # Notice that we declare the type of 'current_user' as the Pydantic model 'User'
    return current_user


# For other type of model: https://fastapi.tiangolo.com/tutorial/security/get-current-user/#other-models


# We just need to add a path operation for the user/client to actually send the username and password. we will talk about this in next one

if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)
