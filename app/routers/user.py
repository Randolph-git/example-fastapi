
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils # use to dots since going to app folder, so outside router 
from ..database import get_db

router = APIRouter(prefix="/users", tags=['Users']) # instead of app = Fastapi

#CREATING A USER
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut) 
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    #hash the password - user.password
    hashed_password = utils.hash(user.password) # hashing passsowrd. reference pwd_context using hash method
    user.password = hashed_password
    
    new_user = models.User(**dict(user)) # 5:14hrs instead of - title =post.title,content = post.content, published = post.published # create new post
    db.add(new_user) # adds the new post to database
    db.commit() # saving to database
    db.refresh(new_user) # similar to returning
    return new_user

#GETTING A USERS ID 6.10hrs
@router.get('/{id}', response_model=schemas.UserOut) # bracket is URL path. id is path parameter and is always a string. user is going to provide a ID of specific post they are interested in
def get_user(id: int, db: Session = Depends(get_db)): #add int as validation in case an error occursfrom the userthen no needfor int in next line. response so that clear error message is given
    user = db.query(models.User).filter(models.User.id == id).first() # filter is similar to WHERE
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"User with id: {id} was not found")
    return user