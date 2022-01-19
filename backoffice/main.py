from dotenv import load_dotenv; load_dotenv()
from fastapi import FastAPI

from .dependencies.utils import create_response, status
from .dependencies.log import logger
from .database.connection import init_db, mock_data

from .routers.modUser.rest import router as user
from .routers.modClient.rest import router as client

app = FastAPI(title="Face Recognizer Backoffice")

@app.on_event("startup")
async def startup():
    logger.info("starting up")

@app.on_event("shutdown")
async def shutdown():
    logger.info("shutting down")

@app.get("/health")
async def health():
    logger.info("check health")
    return create_response(data={"message":"really healthy"}, status=status.success())

@app.get("/restart_db")
async def restart_db():
    logger.info("restart db")
    await init_db()
    await mock_data()
    return create_response(status=status.success())

app.include_router(user, tags=["User"])
app.include_router(client, tags=["Client"])