from fastapi import APIRouter, Request, Path, Query, Header, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Optional, List
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from .controller import crud, login_with_jwt
from ...dependencies.utils import create_response, create_status
from ...dependencies.log import logger
from ...dependencies.utility import CommonQueryGetter
from ...dependencies.hash import encrypt
from ...database.connection import get_session
from ...auth.authBearer import JWTBearer

router = APIRouter(prefix="/v1/user")


class UserPydantic(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=3, max_length=100)
    email: str = Field(min_length=3, max_length=100)

@router.get("/login")
async def login(
        userEmail: str,
        password: str,
        session: AsyncSession = Depends(get_session)
    ):
    return await login_with_jwt(userEmail, password, session)

@router.get("", dependencies=[Depends(JWTBearer())])
async def get_user(
    request: Request,
    getParams=Depends(CommonQueryGetter),
    session: AsyncSession = Depends(get_session)
):
    return await crud.read(getParams, session)

@router.post("", dependencies=[Depends(JWTBearer())])
async def create_user(
    request: Request,
    user: UserPydantic,
    session: AsyncSession = Depends(get_session),
):
    user.password = encrypt(user.password)
    return await crud.create(user, session)


@router.put("/{id}", dependencies=[Depends(JWTBearer())])
async def update_user(
    request: Request,
    user: UserPydantic,
    id: int = Path(..., min=1),
    session: AsyncSession = Depends(get_session),
):
    return await crud.update(user, id, session)


@router.delete("/{id}", dependencies=[Depends(JWTBearer())])
async def delete_user(
    request: Request,
    id: int = Path(..., min=1),
    session: AsyncSession = Depends(get_session),
):
    return await crud.delete(id, session)
