import pymysql
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ...dependencies.log import logger
from ...dependencies.utils import create_response, create_status, BaseCRUD, status
from ...database import models, connection
from ...auth.validator import validate
from ...auth.authHandler import signJWT

crud = BaseCRUD(models.User)

async def login_with_jwt(userEmail, password, session):
    try:
        data = await validate(session, userEmail, password)
        if data:
            access_token = signJWT(userEmail)
            return create_response(data={"access_token":access_token}, status=status.success())
        return create_response(status=status.not_authorized())
    except Exception as e:
        logger.error(e)
        return create_response(status=status.error(e))