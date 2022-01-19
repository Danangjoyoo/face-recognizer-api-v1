from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies.hash import verify
from ..dependencies.log import logger
from ..database import models

async def validate(session: AsyncSession, userEmail: str, password: str):
    try:
        ## check username
        query = select(models.User).where(models.User.username==userEmail)
        data = await session.execute(query)
        data = data.scalars().first()
        if data:
            if verify(password, data.password):
                return data

        ## check email
        query = select(models.User).where(models.User.email==userEmail)
        data = await session.execute(query)
        data = data.scalars().first()
        if data:
            if verify(password, data.password):
                return data
    except Exception as e:
        logger.error(e)

async def validate_token(session: AsyncSession, token: str):
    try:
        query = select(models.Client).where(models.Client.key==token)
        data = await session.execute(query)
        data = data.scalars().first()
        return bool(data)
    except Exception as e:
        logger.error(e)
        return False