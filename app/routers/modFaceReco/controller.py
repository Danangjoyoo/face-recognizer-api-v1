import os, sys, time
from fastapi import UploadFile, Request
from pydantic import BaseModel

from ...helper.classifier import FaceDetection
from ...helper.reader import read_image
from ...dependencies.log import logger
from ...dependencies.utils import BaseCRUD, create_response, status
from ...auth.validator import validate_token
from ...database import models

clientCrud = BaseCRUD(models.Client)

class UpdateClientHit(BaseModel):
    totalHit: int

async def validate_and_recognize(token, file, modelType, confThresh, session):
    try:
        validClient = await validate_token(session, token)
        if not validClient:
            return create_response(status=status.invalid_token())

        clientHit = UpdateClientHit(totalHit=validClient.totalHit+1)
        await clientCrud.update(clientHit, validClient.id, session)

        totalFace = await recognize_face(file, modelType, confThresh)
        
        return create_response(
            data={"total":totalFace},
            meta={"filename":file.filename},
            status=status.success())

    except Exception as e:
        logger.error(e)
        return create_response(status=status.error(e))

async def recognize_face(file: UploadFile, modelType, confidenceThresh):
    image = await read_image(file)
    engine = FaceDetection(0, modelType, confidenceThresh)
    totalFace = engine.count(image)
    return totalFace