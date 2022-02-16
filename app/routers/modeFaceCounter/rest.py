from fastapi import APIRouter, File, UploadFile, Query, Depends, Header, Request
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field

from ...auth.validator import validate_request_token
from ...dependencies.utils import status, create_response
from ...database.connection import get_session
from . import controller

router = APIRouter(prefix="/simple-face-counter")


@router.post("/with_token", dependencies=[Depends(validate_request_token)])
async def count_face(
        file: UploadFile = File(...),
        modelType: int = Query(default=0, ge=0, le=1),
        confidenceThresh: float = Query(default=0.5, ge=0.01, le=0.99),
        session: AsyncSession = Depends(get_session)
    ):
    return await controller.count_face(file, modelType, confidenceThresh, session)

@router.post("")
async def count_face_free(
        file: UploadFile = File(...),
        modelType: int = Query(default=0, ge=0, le=1),
        confidenceThresh: float = Query(default=0.5, ge=0.01, le=0.99),
        session: AsyncSession = Depends(get_session)
    ):
    return await controller.count_face(file, modelType, confidenceThresh, session)