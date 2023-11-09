
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# from dotenv import load_dotenv

# load_dotenv()


# venv\Scripts\activate.bat - to change to venev in command propmt.   uvicorn main:app - to start the server, 
# uvicorn app.main:app --reload after to keep reloading server

#pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto") # we are telling passlib what hashing algorithm we want to use 
#models.Base.metadata.create_all(bind=engine) #tells sqlalchemy to run create statement to generate all the models =  tables. 
                                            # We do not need this now since we are using alembic


app = FastAPI() # create instance of fast api

origins = ["*"] # allows all domains to access the API
#origins = ["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) # middleware is a function that run beforeevery request. 
  # allow_origins = list of origins that can access the API. which domains are allowed
    # allow_credentials = allows us to send cookies to the API.
    # allow_methods = allows us to send requests to the API.so alllow only get requests for e.g
    # allow_headers = allows us to send headers to the API.
                                                

app.include_router(post.router) # prompts search in post file for path operation
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

#below not needed either but he left it
# path operation or route - the order of path operation matters. The first one will always run
@app.get("/") # a decorator (@), which makes the "function" an API operation using the "get" http method. item in bracket is root path
async def root(): # the function; async = asynchronous, optional here
    return {"message": "welcome to randy api"}


















