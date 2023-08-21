import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
import models
import schemas
from database import SessionLocal, engine
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

# create the database tables
models.Base.metadata.create_all(bind=engine)

"""
*) Create a Dependency
    -> Now use the 'SessionLocal' class we created in the 'sql_app/database.py' file to create a dependency.
    -> We need to have an independent database session/connection ('SessionLocal') per request, use the same session through all the request and then close it after the request is finished
    -> And then a new session will be created for the next request.
    -> For that, we will create a new dependency with yield, as explained before in the section about Dependencies with yield (https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/).
    -> Our dependency will create a new SQLAlchemy SessionLocal that will be used in a single request, and then close it once the request is finished.
"""


# Dependency
def get_db():
    db = SessionLocal()
    # We put the creation of the SessionLocal() and handling of the requests in a try block.
    try:
        yield db
    finally:
        # And then we close it in the finally block.
        # This way we make sure the database session is always closed after the request. Even if there was an exception while processing the request.
        # But you can't raise another exception from the exit code (after yield). See more in Dependencies with yield and HTTPException (https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/#dependencies-with-yield-and-httpexception)
        db.close()


"""
*) Alembic Note:
    -> Normally you would probably initialize your database (create tables, etc) with Alembic(https://alembic.sqlalchemy.org/en/latest/).
    -> And you would also use Alembic for "migrations" (that's its main job).
    -> A "migration" is the set of steps needed whenever you change the structure of your SQLAlchemy models, add a new attribute, etc. to replicate those changes in the database, add a new column, a new table, etc.
    -> You can find an example of Alembic in a FastAPI project in the templates from (https://fastapi.tiangolo.com/project-generation/) Specifically in the alembic directory in the source code (https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/alembic/).
"""


@app.get('/')
async def index():
    return "Hello World"


# And then, when using the dependency in a path operation function, we declare it with the type 'Session' we imported directly from SQLAlchemy.
# This will then give us better editor support inside the path operation function, because the editor will know that the 'db' parameter is of type 'Session'
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # The parameter 'db' is actually of type 'SessionLocal', but this class (created with 'sessionmaker()') is a "proxy" of a SQLAlchemy 'Session', so, the editor doesn't really know what methods are provided.
    # But by declaring the type as 'Session', the editor now can know the available methods (.add(), .query(), .commit(), etc) and can provide better support (like completion). The type declaration doesn't affect the actual object.
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # We are creating the database session before each request in the dependency with 'yield', and then closing it afterwards.
    # And then we can create the required dependency in the path operation function, to get that session directly.
    # With that, we can just call 'crud.get_user' directly from inside of the path operation function and use that session.
    users = crud.get_users(db, skip=skip, limit=limit)
    # Notice that the values you return are SQLAlchemy models, or lists of SQLAlchemy models.
    # But as all the path operations have a response_model with Pydantic models / schemas using orm_mode, the data declared in your Pydantic models will be extracted from them and returned to the client, with all the normal filtering and validation.
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Notice that the values you return are SQLAlchemy models, or lists of SQLAlchemy models.
    # But as all the path operations have a response_model with Pydantic models / schemas using orm_mode, the data declared in your Pydantic models will be extracted from them and returned to the client, with all the normal filtering and validation.
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


# About def vs async def: https://fastapi.tiangolo.com/tutorial/sql-databases/#about-def-vs-async-def

def main():
    uvicorn.run("main:app", port=PORT, reload=True)


if __name__ == "__main__":
    main()
