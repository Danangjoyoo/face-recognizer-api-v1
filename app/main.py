from dotenv import load_dotenv; load_dotenv()
from fastapi import FastAPI

from .dependencies.utils import create_response, status
from .dependencies.log import logger
from .database.connection import create_db, mock_data

from .routers.modeFaceCounter.rest import router as faceReco

app = FastAPI(title="Face Recognizer Application")

@app.on_event("startup")
async def startup():
    logger.info("starting up")
    await create_db()
    await mock_data()

@app.on_event("shutdown")
async def shutdown():
    logger.info("shutting down")

@app.get("/health")
async def health():
    logger.info("check health")
    return create_response(data={"message":"really healthy"}, status=status.success())

app.include_router(faceReco, tags=["Face Recognition"])