from dtos.dto_tools import dataclass_to_json
from dataclasses import dataclass

from starlette import status
from typing import Dict, Any, Literal
from typing_extensions import Self

from models.login_models import User

@dataclass
class UserInfoOutDto:
    id:str
    name:str
    infos:str
    rights:str
    def to_json(self) -> str:
        return dataclass_to_json(self)

    @staticmethod
    def user_to_dto(user:User) -> Self:
        return UserInfoOutDto(uuid=user.uuid,name=user.username, user_infos=user.user_infos,user_rights=user.user_rights)


@dataclass
class RefreshTokenOutDto:
    user_uuid:str
    refresh_token:str
    def to_json(self) -> str:
        return dataclass_to_json(self)

@dataclass(init=False)
class AccessTokenOutDto:
    access_token: str 
    refresh_token: str
    data: Dict
    message: str = "User Logged in Successfully."
    token_type: str = "Bearer"
    status: int = status.HTTP_200_OK

    def __init__(self, access_token:str, refresh_token:str, data:User):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.data = data




@dataclass
class MessageDto:
    message:str
    status: int = status.HTTP_200_OK