from fastapi import FastAPI
from app.routers import kinorium
from contextlib import asynccontextmanager
from app.core.http_client import http_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager to handle startup and shutdown events"""

    http_client.start()
    yield
    await http_client.stop()

app = FastAPI(lifespan=lifespan)


app.include_router(kinorium.router)