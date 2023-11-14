
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import Field, SQLModel, create_engine, Session, select, or_, col, text, Relationship, Column, String, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import sessionmaker
from typing import Annotated
from fastapi import FastAPI, Query,  Path, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from config.configuration_settings import retrieve_settings

app = FastAPI()

#  change this
@app.on_event("startup")
async def init_models():
    settings = retrieve_settings()
    async with engine.begin() as conn:
        if settings.DELETE_DB:
            await conn.run_sync(SQLModel.metadata.drop_all)
        if settings.CREATE_DB:
            await conn.run_sync(SQLModel.metadata.create_all)



def create_sqlmodel_engine(create_db = True):
    sqlite_file_name = "database.db"
    sqlite_url = f"sqlite+aiosqlite:///{sqlite_file_name}"

    # engine = create_engine(sqlite_url, echo=True)
    engine = create_async_engine(sqlite_url, echo=True)

    # if create_db:
    #     asyncio.run(init_models())
        # SQLModel.metadata.create_all(engine)
    return engine

engine = create_sqlmodel_engine(True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]