import uvicorn
from fastapi import FastAPI

PORT = 8080
app = FastAPI()

# NOTE: This method of Database integration is older and the documentation is about to get update with having 'SQLModel'(https://sqlmodel.tiangolo.com/)
# But also we can use this way to interact with database

"""
    -> Here we will see example using 'SQLAlchemy'(https://www.sqlalchemy.org/)
    -> You can easily adapt it to any database supported by SQLAlchemy, like:
        -> PostgreSQL
        -> MySQL
        -> SQLite
        -> Oracle
        -> Microsoft SQL Server, etc.
    -> In this example, we'll use SQLite, because it uses a single file and Python has integrated support. So, you can copy this example and run it as is. Later, for your production application, you might want to use a database server like PostgreSQL.

    *) ORMs
        -> https://fastapi.tiangolo.com/tutorial/sql-databases/#orms
        -> Common ORMs are for example: Django-ORM (part of the Django framework), SQLAlchemy ORM (part of SQLAlchemy, independent of framework) and Peewee (independent of framework), among others.
        
    => File Structure:
        .
        └── sql_app
            ├── __init__.py
            ├── crud.py
            ├── database.py
            ├── main.py
            ├── models.py
            └── schemas.py
        
        -> The file __init__.py is just an empty file, but it tells Python that sql_app with all its modules (Python files) is a package.
    
    => Install SQLAlchemy:
        -> pip install sqlalchemy
"""


@app.get('/')
async def index():
    return "Hello World"


if __name__ == "__main__":
    uvicorn.run("main:app", port=PORT, reload=True)
