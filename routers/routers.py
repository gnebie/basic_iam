from fastapi import APIRouter

default_router = APIRouter(
    prefix="",
    tags=["default"]
)

auth_router_v1 = APIRouter(
    prefix="/v1/auth",
    tags=["auth"]
)

admin_router_v1 = APIRouter(
    prefix="/admin/v1/auth",
    tags=["admin"]
)
