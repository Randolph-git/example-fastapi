from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl= 'login')

#secret key
SECRET_KEY = settings.secret_key 

# Algorithm
ALGORITHM = settings.algorithm

# Expiration time to make sure useer is not logged in forever
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy() # making a copy of variable data

    #expiration field
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # get current time and add 30 min
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # create jwt token
    return encoded_jwt

# fxn to verify the access token that was created
def verify_access_token(token: str, credentials_exception): # credentials_excep is variablein case verification does not work
    
    # always use try if code could generate error
    try:
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise credentials_exception
    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
    detail=f"could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    
    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    return user

