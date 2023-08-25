from fastapi import FastAPI, Depends, HTTPException, status
import uvicorn
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from pydantic import BaseModel

app = FastAPI()
PORT = 8080

# This is the fake DB with let's say 'user' table
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

# Get the username and password first
# OAuth2 specifies that when using the "password flow" (that we are using) the client/user must send a username and password fields as form data.
# The spec also states that the username and password must be sent as form data (so, no JSON here).


# 'scope': https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/#scope


# Code to get the username and password

# First, import 'OAuth2PasswordRequestForm', and use it as a dependency with 'Depends' in the path operation for '/token'


def fake_hash_password(password: str):
    # function where we will implement hashing password but for now we will fake it
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# now can access '/token' url to get the token


# Create a user Base model that doesn't have password file
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    # User Fake Database Model that contain actual password
    hashed_password: str


def get_user(db, username: str):
    # 'db' is 'fake_users_db'
    if username in db:
        # here we are checking the username, if it exist with the given 'username' then we will extract the information of that user from the db in this case 'fake_users_db'
        user_dict = db[username]
        # and returning the user with 'UserInDB' Type
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    # here we are getting the user by passing the 'fake_users_db' and 'token'
    # Note that 'token' that we are passing for now is the user 'username' value
    user = get_user(fake_users_db, token)
    # and if after decoding and finding the user it will return the user
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    # We want to get the 'current_user' only if this user is active.
    # So, we create an additional dependency get_current_active_user that in turn uses 'get_current_user' as a dependency.
    # So, in our endpoint that uses this 'get_current_active_user' as dependencies, we will only get a user if the user exists, was correctly authenticated, and is active:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# This endpoint is what we will use to login or authenticate the user which will get 'username' & 'password' and return the token if user exist
@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # OAuth2PasswordRequestForm is a class dependency that declares a form body with:
    #   -> The username.
    #   -> The password.
    #   -> An optional scope field as a big string, composed of strings separated by spaces.
    #   -> An optional grant_type.
    # The OAuth2 spec actually requires a field 'grant_type' with a fixed value of 'password', but OAuth2PasswordRequestForm doesn't enforce it.
    # If you need to enforce it, use 'OAuth2PasswordRequestFormStrict' instead of 'OAuth2PasswordRequestForm'.

    # from from_data we will going to get the 'username' & 'password' first we will going tog et the user information from the 'fake_users_db'
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    # If user exist then we will going to create the 'UserInDB' type from user information
    user = UserInDB(**user_dict)
    # Above equivalent is:
    # UserInDB(
    #     username = user_dict["username"],
    #     email = user_dict["email"],
    #     full_name = user_dict["full_name"],
    #     disabled = user_dict["disabled"],
    #     hashed_password = user_dict["hashed_password"],
    # )

    # and we will hash the password that user send
    hashed_password = fake_hash_password(form_data.password)

    # if uer hash password and the db hash password get match we will going to validated the user
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    # here we are passing user 'username' as token value
    # the type of token
    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    # Endpoint that uses 'get_current_active_user' and return 'current_user' if exist
    return current_user


# Using Above way, you can make the security system compatible with any database and with any user or data model.
# The only detail missing is that it is not actually "secure" yet.
# In the next chapter we'll see how to use a secure password hashing library and JWT tokens.

if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)
