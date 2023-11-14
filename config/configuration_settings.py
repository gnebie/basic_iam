
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

class AuthSettings:
    ACCESS_TOKEN_SECRET_KEY: str = "abcdef1234"
    REFRESH_TOKEN_SECRET_KEY: str = "abcdef1234"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 10  # in mins
    REFRESH_TOKEN_EXPIRE_MINUTES = 60*24  # in mins
    COOKIE_NAME = "access_token"
    CREATE_DB = True
    DELETE_DB = True

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oath2_bearer = OAuth2PasswordBearer(tokenUrl='v1/auth/token')

settings = AuthSettings()

def retrieve_settings():
    return settings