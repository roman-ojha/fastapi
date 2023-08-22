# In this file we will have reusable functions to interact with the data in the database.


# Import 'Session' from 'sqlalchemy.orm', this will allow you to declare the type of the 'db' parameters and have better type checks and completion in your functions.
from sqlalchemy.orm import Session

# Import 'models' (the SQLAlchemy models) and 'schemas' (the Pydantic models / schemas).
import models
import schemas


# Function to read single user by Id
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# Function to read single user by email


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Function to get list of users


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# Function to create new user


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    # Create a SQLAlchemy model instance with your data.
    db_user = models.User(
        email=user.email, password=fake_hashed_password)
    # add that instance object to your database session.
    db.add(db_user)
    # commit the changes to the database (so that they are saved).
    db.commit()
    # refresh your instance (so that it contains any new data from the database, like the generated ID).
    db.refresh(db_user)
    return db_user


# Function to get list of items
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


# Function to create new item
def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.model_dump(), owner_id=user_id)
    # Instead of passing each of the keyword arguments to Item and reading each one of them from the Pydantic model, we are generating a dict with the Pydantic model's data with 'item.model_dump()'
    # and then we are passing the dict's key-value pairs as the keyword arguments to the SQLAlchemy Item, with 'Item(**item.model_dump())'
    # And then we pass the extra keyword argument 'owner_id' that is not provided by the Pydantic model
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# By creating functions that are only dedicated to interacting with the database (get a user or an item) independent of your path operation function, you can more easily reuse them in multiple parts and also add unit tests for them.


"""
=> Tips:
    -> The SQLAlchemy model for 'User' contains a 'password' that should contain a secure hashed version of the password.
    -> But as what the API client provides is the original password, you need to extract it and generate the hashed password in your application.
    -> And then pass the 'password' argument with the value to save.

=> Warning
    -> This example is not secure, the password is not hashed.
    -> In a real life application you would need to hash the password and never save them in plaintext.
    -> For more details, go back to the Security section in the tutorial.
    -> Here we are focusing only on the tools and mechanics of databases.
"""
