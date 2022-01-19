from fastapi import APIRouter, File, UploadFile, Query, Depends, Header, Request
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field

from ...auth.validator import validate_request_token
from ...dependencies.utils import status, create_response
from ...database.connection import get_session
from .controller import validate_and_recognize

router = APIRouter(prefix="/simple-face-reco")


@router.post("", dependencies=[Depends(validate_request_token)])
async def count_face(
        token: str = Header(...),
        file: UploadFile = File(...),
        modelType: int = Query(default=0, ge=0, le=1),
        confidenceThresh: float = Query(default=0.5, ge=0.01, le=0.99),
        session: AsyncSession = Depends(get_session)
    ):
    return await validate_and_recognize(token, file, modelType, confidenceThresh, session)