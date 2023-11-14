

from services.login import *
from routers.routers import admin_router_v1
from dtos.login_dto import UserInfoOutDto, MessageDto
from starlette import status
from fastapi import HTTPException

@admin_router_v1.get("/users")
async def user_list(db: db_dependency, skip: int = 0, limit: int = 10) -> List[UserInfoOutDto]: # pagination
    list_users = await db.exec(select(User).where().offset(skip).limit(limit))
    list_users = list_users.all()
    return [UserInfoOutDto.user_to_dto(user) for user in  list_users]

@admin_router_v1.get("/user/{user_id}")
async def get_user(db: db_dependency, user_name) -> UserInfoOutDto:
    user = await get_user_by_name(db, user_name)
    return UserInfoOutDto.user_to_dto(user)

@admin_router_v1.post("/user/{user_id}", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest) -> None:
    await create_new_user(create_user_request, db)


@admin_router_v1.put("/user/{user_id}")
async def modify_user(user_id:str) -> None:
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Method not create yet.") 

@admin_router_v1.delete("/user/{user_id}")
async def delete_user(db: db_dependency, user_id:str) -> None:
    user = await get_user_by_name(db, user_id)
    db.delete(user)
    db.commit()
