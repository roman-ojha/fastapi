from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite::///./database.db"

# For different database like pastgresql
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# Create alchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    # the argument: connect_args={"check_same_thread": False} is only needed for SQLite. It's not needed for other database.
    # By default SQLite will only allow one thread to communicate with it, assuming that each thread would handle an independent request.
    # This is to prevent accidentally sharing the same connection for different things (for different requests).
    # But in FastAPI, using normal functions (def) more than one thread could interact with the database for the same request, so we need to make SQLite know that it should allow that with connect_args={"check_same_thread": False}.
    # Also, we will make sure each request gets its own database connection session in a dependency, so there's no need for that default mechanism.
)

# Each instance of the 'SessionLocal' class will be a database session. The class itself is not a database session yet.
# But once we create an instance of the 'SessionLocal' class, this instance will be the actual database session.
# We name it 'SessionLocal' to distinguish it from the 'Session' we are importing from SQLAlchemy.
# We will use 'Session' (the one imported from SQLAlchemy) later.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Now we will use the function 'declarative_base()' that returns a class.
# Later we will inherit from this class to create each of the database models or classes (the ORM models)
Base = declarative_base()
