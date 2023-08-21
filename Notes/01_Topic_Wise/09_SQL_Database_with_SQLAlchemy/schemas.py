# To avoid confusion between the SQLAlchemy models and the Pydantic models, we will have the file 'models.py' with the SQLAlchemy models, and the file 'schemas.py' with the Pydantic models.
# These Pydantic models define more or less a "schema" (a valid data shape).
# So this will help us avoiding confusion while using both.

"""
*) Created initial Pydantic models/Schemas
    -> Create an 'ItemBase' and 'UserBase' Pydantic models (or let's say "schemas") to have common attributes while creating or reading data.
    -> And create an 'ItemCreate' and 'UserCreate' that inherit from them (so they will have the same attributes), plus any additional data (attributes) needed for creation.
    -> So, the user will also have a 'password' when creating it.
    -> But for security, the 'password' won't be in other Pydantic models, for example, it won't be sent from the API when reading a user.
"""

from pydantic import BaseModel


# Now create Pydantic models (schemas) that will be used when reading data, when returning it from the API.
class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass

# For example, before creating an item, we don't know what will be the ID assigned to it, but when reading it (when returning it from the API) we will already know its ID.


class Item(ItemBase):
    id: int
    owner_id: int

    # Now, in the Pydantic models for reading, 'Item' and 'User', we have to add an internal Config class.
    # This Config(https://pydantic-docs.helpmanual.io/usage/model_config/) class is used to provide configurations to Pydantic.
    # Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict, but an ORM model (or any other arbitrary object with attributes).
    # This way, instead of only trying to get the id value from a dict, as in:
    #   -> id = data["id"]
    # it will also try to get it from an attribute, as in:
    #   -> id = data.id
    # And with this, the Pydantic model is compatible with ORMs, and you can just declare it in the 'response_model' argument in your path operations.
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):  # While creating we just need to pass 'email', 'password'
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []
    # The same way, when reading a user, we can now declare that 'items' will contain the items that belong to this user.
    # Not only the IDs of those items, but all the data that we defined in the Pydantic model for reading items: Item

    class Config:
        orm_mode = True

    # Notice that the User, the Pydantic model that will be used when reading a user (returning it from the API) doesn't include the password.


"""
*) Technical Detail About ORM mode:
    -> SQLAlchemy and many others are by default "lazy loading".
    -> That means, for example, that they don't fetch the data for relationships from the database unless you try to access the attribute that would contain that data.
    -> For example, accessing the attribute 'items':
        -> current_user.items
    -> would make SQLAlchemy go to the 'items' table and get the items for this user, but not before.
    -> Without 'orm_mode', if you returned a SQLAlchemy model from your path operation, it wouldn't include the relationship data.
    -> Even if you declared those relationships in your Pydantic models.
    -> But with ORM mode, as Pydantic itself will try to access the data it needs from attributes (instead of assuming a 'dict'), you can declare the specific data you want to return and it will be able to go and get it, even from ORMs.
"""
