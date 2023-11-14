
from tools.string_tools import get_random_string

from config.configuration_settings import retrieve_settings, bcrypt_context, oath2_bearer
from models.login_models import *
from models.create_models import *
import datetime as dt
from jose import jwt, JWSError, JWTError

from typing import Dict
from exceptions.login_exceptions import unauthorized_exception
from config import constants
from dtos.login_dto import AccessTokenOutDto

settings = retrieve_settings()

async def get_current_user(token: Annotated[str, Depends(oath2_bearer)]):
    try:
        payload = jwt.decode(token, settings.ACCESS_TOKEN_SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("name")
        uuid: str = payload.get("id")
        if username is None or uuid is None:
            raise unauthorized_exception("Invalid token")
        return {"username":username, "uuid":uuid}
    except JWTError:
        raise unauthorized_exception("Invalid or expired token")

user_dependency = Annotated[dict, Depends(get_current_user)]


async def create_new_user(user_request : CreateUserRequest, db):
    presalt = get_random_string(constants.PRESALT_SIZE)
    postsalt = get_random_string(constants.POSTSALT_SIZE)
    new_user = User(username= user_request.username, 
                hash_password=bcrypt_context.hash(presalt + user_request.password + postsalt),
                pre_salt=presalt,
                post_salt=postsalt,
                user_infos="", #todo
                user_rights="" #todo
                )
    db.add(new_user)
    await db.commit()
    return new_user


def create_access_token(access_token_data: Dict) -> str:
    """ Encrypt the access jwt

    Args:
        access_token_data (Dict): the access token data

    Returns:
        str: the encrypted jwt
    """
    to_encode = access_token_data.copy()
    expire = dt.datetime.utcnow() + dt.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.ACCESS_TOKEN_SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def create_refresh_token(data: Dict) -> str:
    """
    Create a refresh token with 30 days for expired time (default),
    info for param and return check to function create token

    :return: hash token
    """
    to_encode = data.copy()
    expire = dt.datetime.utcnow() + dt.timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.REFRESH_TOKEN_SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def verify_the_token(token:str, secret:str, algorithm:str):
    """ verify the jwt

    Args:
        token (str): jwt
        secret(str): secret_key
        algorithm(str): algorithm used

    Raises:
        unauthorized_exception: user id not found
        unauthorized_exception: JWT extraction error

    Returns:
        Dict: The JWT data
    """
    try:
        payload = jwt.decode(token, secret, algorithms = algorithm)
        id:str = payload.get("user_uuid")
        if id is None:
            raise unauthorized_exception()
        token_data = RefreshToken(user_uuid=id)
        return token_data
    except JWTError:
        raise unauthorized_exception()


def verify_access_token(token:str) -> Dict:
    """ verify the access jwt

    Args:
        token (str): access jwt

    Raises:
        unauthorized_exception: user id not found
        unauthorized_exception: JWT extraction error

    Returns:
        Dict: The JWT data
    """
    return verify_the_token(token, settings.ACCESS_TOKEN_SECRET_KEY, algorithms=settings.ALGORITHM)


def verify_refresh_token(token:str) -> Dict:
    """ verify the refresh jwt

    Args:
        token (str): refresh jwt

    Raises:
        unauthorized_exception: user id not found
        unauthorized_exception: JWT extraction error

    Returns:
        Dict: The JWT data
    """
    return verify_the_token(token, settings.REFRESH_TOKEN_SECRET_KEY, algorithms=settings.ALGORITHM)


def get_new_access_token(token:str):
    token_data = verify_refresh_token(token)
    return create_access_token(token_data)


# async def get_user_by_username(name:str, db) -> User:
#     user = await db.execute(select(User).filter(User.username == name))
#     user = user.scalars().first()
#     return user
async def get_user_by_name(db, username:str):
    user = await db.exec(select(User).where(User.username == username))
    user = user.first()
    return user

async def get_refresh_token(db, user_uuid):
    refresh_token = await db.execute(select(RefreshToken).filter(RefreshToken.user_uuid == user_uuid))
    refresh_token = refresh_token.scalars().first()
    return refresh_token

async def authentificate_user(name:str, password:str, db) -> User:
    user = get_user_by_name(db, user)
    if user and bcrypt_context.verify(user.pre_salt + password + user.post_salt, user.hash_password): 
        return user
    return False



async def create_token_from_user(db, user):
    # to change => token_infos to a class
    token_infos = {"id":user.uuid, "name":user.username, 
                   "infos":user.user_infos, "rights":user.user_rights}
    token = create_access_token(token_infos)
    return token

async def create_refresh_token_from_user(db, user):
    # to change => ,refresh_token to a class
    refresh_token_info = {"user_uuid":user.uuid}
    
    refresh_token = create_refresh_token(refresh_token_info)
    refresh_token_info["refresh_token"] = refresh_token

    refresh_token_db_data= RefreshToken(**refresh_token_info)

    db.add(refresh_token_db_data)
    db.commit()
    
    return refresh_token

async def delete_refresh_token(db, user:User):
    refresh_token = await get_refresh_token(db, user.uuid)
   
    if refresh_token:
        refresh_token.delete()
        db.commit()

async def check_user_autentification_attempts(user):
    # TODO : can auth more than 1 by second by user
    # get user_by_name()
    # check user last connection tenetative
    pass

async def login_token(db, form_data):
    user = await authentificate_user(form_data.username, form_data.password, db)
    if not user:
        raise unauthorized_exception("User or password invalid")
    await check_user_autentification_attempts(user)
    await delete_refresh_token(db, user)

    # a sortir de la fonction
    token = await create_token_from_user(db, user)
    refresh_token = await create_refresh_token_from_user(db, user)

    # change to a class
    return AccessTokenOutDto(token, refresh_token, user)
    # {
    #     "access_token": token,
    #     "token_type":"Bearer",
    #     "refresh_token": refresh_token,
    #     "message": "User Logged in Successfully.",
    #     "data": user_to_dto(user),
    #     "status": status.HTTP_200_OK
    # }
