from fastapi import FastAPI, Depends
import uvicorn
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

app = FastAPI()
PORT = 8080

# Docs: https://fastapi.tiangolo.com/tutorial/security/first-steps/

# First let's install'python-multipart'(https://andrew-d.github.io/python-multipart/)
# This is because OAuth2 uses "form data" for sending the 'username' and 'password'.

# The 'oauth2_scheme' variable is an instance of OAuth2PasswordBearer, but it is also a "callable".
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# Here tokenUrl="token" refers to a relative URL 'token' that we haven't created yet. As it's a relative URL, it's equivalent to ./token.
# Because we are using a relative URL, if your API was located at https://example.com/, then it would refer to https://example.com/token. But if your API was located at https://example.com/api/v1/, then it would refer to https://example.com/api/v1/token.
# Using a relative URL is important to make sure your application keeps working even in an advanced use case like Behind a proxy (https://fastapi.tiangolo.com/advanced/behind-a-proxy/)


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    # AFter just using the 'oauth2_scheme' we will be able to see the 'Authorize' button on Swagger documentation
    # This dependency 'oauth2_schema' will provide a 'str' that is assigned to the parameter 'token' of the path operation function.
    return {"token": token}


# The 'password' flow : https://fastapi.tiangolo.com/tutorial/security/first-steps/#the-password-flow

# FastAPI's OAuth2PasswordBearer
# FastAPI provides several tools, at different levels of abstraction, to implement these security features.

# When we create an instance of the 'OAuth2PasswordBearer' class we pass in the 'tokenUrl' parameter. This parameter contains the URL that the client (the frontend running in the user's browser) will use to send the 'username' and 'password' in order to get a token.


# What it does?
# It will go and look in the request for that 'Authorization' header, check if the value is Bearer plus some token, and will return the token as a 'str'.
# If it doesn't see an 'Authorization' header, or the value doesn't have a 'Bearer' token, it will respond with a 401 status code error (UNAUTHORIZED) directly.


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)
