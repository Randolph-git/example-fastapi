from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto") # we are telling passlib what hashing algorythm we want to use 

def hash(password: str):
    return pwd_context.hash(password)

# comparing password provided by user with that stored in database
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password,hashed_password) # verify method

