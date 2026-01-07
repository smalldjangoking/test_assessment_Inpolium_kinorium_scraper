from fastapi import APIRouter, status, Query
from app.core.http_client import http_client
from fastapi.responses import JSONResponse
import logging
from schemas.http_scraper import PerPageLimit, Genre

router = APIRouter(prefix="/v1/kinorium", tags=["kinorium service"])


@router.get("/health", status_code=status.HTTP_200_OK)
async def kinorium_health_check():
    """Health check endpoint for external service https://ua.kinorium.com/"""

    try:
        async with http_client.get("https://kinorium.com") as response:
            if response.status != 200:
                 # If status is not 200, log and return BAD status
                 logging.warning(f"External service returned {response.status}")
                 return {
                      "status": "BAD",
                      "message": f"External service returned status {response.status}"
                      }
        
            html = await response.text()
            if "topMenu__logo" in html:
                return {"status": "OK", "message": "ua.kinorium.com is up and running."}
            
            logging.warning("Expected content not found in response.")
            return {
                "status": "BAD", 
                "message": "ua.kinorium.com is down or content has changed."
            }
        
    except Exception as e:
        logging.warning(f"Error during health check: {e}")
        return JSONResponse(
            content={
                "status": "BAD", 
                "message": "Error occurred while checking external service"
            },
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    

@router.get("/scraper/http", status_code=status.HTTP_200_OK)
async def kinorium_via_http_client(
    genre: Genre = Query(default=Genre.FANTASY, description="Genre to filter by"),
    page: int = Query(default=1, ge=1),
    per_page: PerPageLimit = PerPageLimit.SMALL
):
    """Uses the aiohttp HTTP client to fetch data from kinorium.com"""

    return {"message": f"Welcome to the Kinorium service router. Genre: {genre.id}, Page: {page}, Per Page: {per_page}"}