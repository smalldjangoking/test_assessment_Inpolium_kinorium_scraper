import asyncio
from fastapi import FastAPI
from app.routers import kinorium
from contextlib import asynccontextmanager
from app.core.http_client import http_client
from app.core.browser import browser_manager

# Set event loop policy for Windows compatibility
if hasattr(asyncio, 'WindowsProactorEventLoopPolicy'):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager to handle startup and shutdown events"""

    await http_client.start()
    await browser_manager.get_browser(headless=True)
    yield
    await http_client.stop()
    await browser_manager.stop_engine()

app = FastAPI(lifespan=lifespan)


app.include_router(kinorium.router)