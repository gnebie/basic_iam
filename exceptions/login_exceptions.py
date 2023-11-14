from fastapi import HTTPException, WebSocketException
from starlette import status


def unauthorized_exception(detail:str="Could not validate credentials"):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"}        
    )

def forbiden_exception(detail:str="Action fobiden"):
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail) 