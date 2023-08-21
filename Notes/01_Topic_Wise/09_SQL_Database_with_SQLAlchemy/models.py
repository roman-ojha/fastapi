# We will use this Base class we created before to create the SQLAlchemy models.
# SQLAlchemy uses the term "model" to refer to these classes and instances that interact with the database.
# But Pydantic also uses the term "model" to refer to something different, the data validation, conversion, and documentation classes and instances.


# Import Base from database (the file database.py from above).

from .database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


# Creating User Model
class User(Base):
    __tablename__ = "users"  # name of the table in database

    # Defining the Column structure
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    # as we have created many to one relation from 'User' to 'Item' we can access 'item' from this class ORM as well
    items = relationship("Item", back_populates='owner')
    # <field> = relationship("<model>", back_populates='<targeted_field>')
    # When accessing the attribute items in a User, as in my_user.items, it will have a list of Item SQLAlchemy models (from the items table) that have a foreign key pointing to this record in the users table.
    # When you access my_user.items, SQLAlchemy will actually go and fetch the items from the database in the items table and populate them here.


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    # Defining the 'owner_id' field with foreign key of 'User' model of 'id' field
    owner_id = Column(Integer, ForeignKey("users.id"))

    # to access 'User' record that is related to 'Item' record we will use 'owner' field
    owner = relationship("User", back_populates="items")
    # And when accessing the attribute owner in an Item, it will contain a User SQLAlchemy model from the users table. It will use the owner_id attribute/column with its foreign key to know which record to get from the users table.
