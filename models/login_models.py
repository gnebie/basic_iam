
from typing import List, Optional
from pydantic import BaseModel, HttpUrl, Field
import uuid as uuid_pkg

from sqlmodel import Field, SQLModel, text
# from sqlmodel import Field, SQLModel, create_engine, Session, select, or_, col, text, Relationship, Column, String, Integer, ForeignKey, TIMESTAMP
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from enums.user_rights import Rights


class UserRights(BaseModel):
    rights : List[Rights] = []

class UserInfos(SQLModel):
    gender:Optional[int]

class UserDto(BaseModel):
    uuid:uuid_pkg.UUID
    name:str
    user_infos:str#:UserInfos
    user_rights:str#:UserRights

class CreateUserRequest(BaseModel):
    username:str = Field(min_length=6, max_length=40, description="The username must be between 6 and 40.")
    password:str = Field(min_length=10, max_length=40, description="The password size must be betwwen 10 and 40.")


class Token(BaseModel):
    jwt:str
    refresh_token:str


class RefreshToken(SQLModel, table=True):
    # __tablename__ = "refresh_token"
    id:int = Field( primary_key=True, index = True)
    user_uuid:uuid_pkg.UUID = Field(foreign_key="user.uuid", unique=True, index = True)
    refresh_token:str = Field(nullable=False)
    date_created:str = Field(nullable=False, default=text("now()"))
    # user = relationship("User")


class User(SQLModel, table=True):
    uuid:uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    username:str = Field(index=True,  unique=True)
    pre_salt:str = Field(min_length=9, max_length=15, description="The presalt must be between 9 and 15.")
    post_salt:str = Field(min_length=9, max_length=15, description="The postsalt must be between 9 and 15.")  
    hash_password:str  
    user_rights:str#:UserRights  = None
    user_infos:str#: UserInfos = Field()

