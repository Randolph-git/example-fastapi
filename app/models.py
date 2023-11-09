#each model is a table in the database
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey # for the table columns
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"),nullable=False)
                                            #users - tablename, id - id column, Cascade for deleting users

    owner = relationship("User") # tell sqlalchemy to fetch info based on a releationship. returns Class of another model in this case 'User'
                            #fetch the user based on the owner ID so we dont have to manually do it

#user registration
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True) # unique,so email cannot be registered twice
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,server_default=text('now()'))
    phone_number = Column(String)

# voting on posts - create vote table
class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)