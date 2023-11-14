
from routers.routers import auth_router_v1
from services.login import *
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from exceptions.login_exceptions import forbiden_exception
from dtos.login_dto import AccessTokenOutDto, UserInfoOutDto, MessageDto
from starlette import status

# login 
@auth_router_v1.post("/login")
async def login(db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return await login_token(db, form_data)

# login 
@auth_router_v1.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user_request : CreateUserRequest, db: db_dependency) -> UserInfoOutDto:
    user_exist = await get_user_by_name(db, user_request.username)
    if user_exist:
        raise forbiden_exception("Username already exist.") 
    user = await create_new_user(user_request, db)
    return UserInfoOutDto.user_to_dto(user)


@auth_router_v1.post("/token")
async def login_tok(db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return await login_token(db, form_data)


@auth_router_v1.get("/info")
async def user_info(user: user_dependency, db: db_dependency)  -> UserInfoOutDto:
    user = await get_user_by_name(db, user["username"])
    return UserInfoOutDto.user_to_dto(user)


@auth_router_v1.get("/logout") # a tester
async def logout(user: user_dependency, db: db_dependency) -> None:
    await delete_refresh_token(db, user)

@auth_router_v1.post("/refresh")
async def refresh_access_token(db: db_dependency, token:str) -> AccessTokenOutDto:
    return create_access_token(verify_refresh_token(token).dict())
    
@auth_router_v1.post("/check")
async def check_token(db: db_dependency, token:str):
    return verify_access_token(token)

@auth_router_v1.post("/delete-my-account")
async def delete_my_account(user: user_dependency, db: db_dependency) -> None:
    user = await get_user_by_name(db, user["username"])
    db.delete(user)
    db.commit()

@auth_router_v1.post("/change_password")
async def change_password(user: user_dependency, db: db_dependency, password) -> MessageDto:
    user = await get_user_by_name(db, user["username"])
    user.hash_password=bcrypt_context.hash(user.pre_salt + password + user.post_salt)
    db.commit()
    return MessageDto("passord change successfuly")

