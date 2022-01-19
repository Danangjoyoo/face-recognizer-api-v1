import time
from fastapi import APIRouter, Request, Path, Query, Header, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Optional, List
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from .controller import crud
from ...dependencies.utils import create_response, create_status
from ...dependencies.log import logger
from ...dependencies.utility import CommonQueryGetter
from ...dependencies.hash import encrypt
from ...database.connection import get_session
from ...auth.authBearer import JWTBearer

router = APIRouter(prefix="/v1/client", dependencies=[Depends(JWTBearer())])


class ClientPydantic(BaseModel):
    name: str = Field(..., max_length=100)
    keybase: str = Field(default="",max_length=255)
    active: bool = Field(default=True)
    totalHit: Optional[int]

@router.get("")
async def get_client(
    request: Request,
    getParams=Depends(CommonQueryGetter),
    session: AsyncSession = Depends(get_session)
):
    return await crud.read(getParams, session)

@router.post("")
async def create_client(
    request: Request,
    client: ClientPydantic,
    session: AsyncSession = Depends(get_session),
):
    key = encrypt(client.name+client.keybase+str(time.time()))
    client.__dict__["key"] = key
    del client.__dict__["keybase"]
    return await crud.create(client, session)


@router.put("/{id}")
async def update_client(
    request: Request,
    client: ClientPydantic,
    id: int = Path(..., min=1),
    session: AsyncSession = Depends(get_session),
):
    key = encrypt(client.name+client.keybase+str(time.time()))
    client.__dict__["key"] = key
    del client.__dict__["keybase"]
    if not client.totalHit: del client.__dict__["totalHit"]
    return await crud.update(client, id, session)


@router.delete("/{id}")
async def delete_client(
    request: Request,
    id: int = Path(..., min=1),
    session: AsyncSession = Depends(get_session),
):
    return await crud.delete(id, session)
