# this file is for the environment variables which you can set on your machine
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

# # you can add default values if you want
class Settings(BaseSettings):   
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    
settings = Settings()
print(settings)

#tell pydantic to import from .env file
    # class config:
    #     env_file = ".env"






