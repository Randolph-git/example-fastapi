from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

#connecting to the database - using connection string
SQIALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# use the engine so that sqlalchemy can connect to postgres database
engine = create_engine(SQIALCHEMY_DATABASE_URL)
#however to talk to the SQL database use session
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

Base = declarative_base() # all models defined for creating tables will extend Base class


# Dependency - open and close a session each. session object responsible for talikng to database
# was intially in main.py - so import it into main file
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


