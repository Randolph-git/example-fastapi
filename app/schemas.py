from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

# this is a schema
class PostBase(BaseModel): # to validate information from client (front end)
    title: str
    content: str
    published: bool = True # if user does not provide this it defaults to true
    #rating: Optional[int] = None #if rating is optional for user to input 

class PostCreate(PostBase): # inheritance
    pass # this takes everything from the above
    
#response to the user
class UserOut (BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        #orm_mode = True
        from_attributes = True

#Sending data back to user with response. leys you control what data to send back
class Post(PostBase): #inheritance
    id: int
    created_at: datetime
    owner_id: int # return here to understand wy put this here 8:16hrs
    owner: UserOut # return a pydantic  model. added to return user information. it will automatically get info in UserOut class above

class Config:
    #orm_mode = True #pydantic works with dictionaries so need ORM_mode = true
    from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    # class Config: #does not seem to be needed here
    # from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr # emailstr ensures its a valid email
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
# for access token
class Token(BaseModel):
    access_token: str
    token_type: str

# for token data that was embeded in the token, here was id
class TokenData(BaseModel):
    #id: Optional[str] = ""
    id: int

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # direction. conint is a pydantic validator. conint(le=1) means that the value must be less than or equal to 1.  but adds negative figures
                        # makes sure its either 0 or 1.
