import os
from ..dependencies.log import logger
from .models import Base
from . import models

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

import json

DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def insert_data(dataModel, session=None):
    if not session:
        async with async_session() as session:
            session.add(dataModel)
            await session.commit()
            await session.refresh(dataModel)
    else:
        session.add(dataModel)
        await session.commit()
        await session.refresh(dataModel)


async def update_data(session, tableModel, dataObject, newDataPydantic):
    updates = {}
    fields = [i for i in vars(tableModel) if "_" not in [i[0], i[-1]]]
    for key in fields:
        if key in newDataPydantic.__dict__:
            updates[key] = newDataPydantic.__dict__[key]
    for key, value in updates.items():
        setattr(dataObject, key, value)
    session.add(dataObject)
    await session.commit()
    await session.refresh(dataObject)

async def mock_data():
    await insert_data(models.User(username="joy", password="$2b$12$81BVmiTZHO.UqWEgzUKvdeD2CClimoq.eoyiGDyIv/KkOjOh4Yz3m", email="joy@gmail.com"))
    await insert_data(models.Client(
            name="MNC-DSM",
            key="$2b$12$x/LYvtDA/pz4IZN4zGXVtuetifXJflyaMYCIvimsEWJOExVQHL8XW"
            )
        )