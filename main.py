from fastapi import FastAPI
import uvicorn

from routers.routers import admin_router_v1, auth_router_v1, default_router
from controllers import *

app = FastAPI() 


app.include_router(admin_router_v1)
app.include_router(auth_router_v1)
app.include_router(default_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)