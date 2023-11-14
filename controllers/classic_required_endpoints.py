
from routers.routers import default_router
from config.versions import versions
from fastapi import FastAPI, Request

# default urls 
@default_router.get("/")
async def root():
    return {"message": "Welcome"}


@default_router.get("/versions")
async def version():
    return [{"version": version, "baseurl": "/v1"}]

# retrieve all unknown paths
@default_router.api_route("/{path_name:path}", methods=["GET"])
async def catch_all(request: Request, path_name: str):
    return {"request_method": request.method, "path_name": path_name}
