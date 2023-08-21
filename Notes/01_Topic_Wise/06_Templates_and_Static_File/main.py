from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
# You could also use from starlette.staticfiles import StaticFiles.
# FastAPI provides the same starlette.staticfiles as fastapi.staticfiles just as a convenience for you, the developer. But it actually comes directly from Starlette.
from fastapi.templating import Jinja2Templates
"""
*) Static File
    -> You can serve static files automatically from a directory using StaticFiles.

*) Mounting:
    -> "Mounting" means adding a complete "independent" application in a specific path, that then takes care of handling all the sub-paths.
    -> This is different from using an APIRouter as a mounted application is completely independent. The OpenAPI and docs from your main application won't include anything from the mounted application, etc.

"""

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name="static")
# The first "/static" refers to the sub-path this "sub-application" will be "mounted" on. So, any path that starts with "/static" will be handled by it.
# The directory="static" refers to the name of the directory that contains your static files.
# The name="static" gives it a name that can be used internally by FastAPI.

"""
*) Template:
    -> You can use any template engine you want with FastAPI.
    -> A common choice is Jinja2, the same one used by Flask and other tools.
    -> There are utilities to configure it easily that you can use directly in your FastAPI application (provided by Starlette).
    => Install jinja2: https://jinja.palletsprojects.com/en/2.10.x/
        -> pip install jinja2
"""

templates = Jinja2Templates(directory="templates")
# Use the templates you created to render and return a TemplateResponse, passing the request as one of the key-value pairs in the Jinja2 "context".


@app.get("/", response_class=HTMLResponse)
# By declaring response_class=HTMLResponse the docs UI will be able to know that the response will be HTML.
async def read_user(request: Request):
    context = {'request': request, 'name': "Roman Ojha"}
    # Notice that you have to pass the request as part of the key-value pairs in the context for Jinja2. So, you also have to declare it in your path operation.
    return templates.TemplateResponse("index.html", context=context)

# For Template check out this docs:
# -> Starlette: https://www.starlette.io/templates/
# -> Jinja: https://jinja.palletsprojects.com/en/2.10.x/
