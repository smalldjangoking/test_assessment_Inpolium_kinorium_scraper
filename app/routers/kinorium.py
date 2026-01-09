from fastapi import APIRouter, status, Query
from fastapi.responses import JSONResponse
import logging
from app.schemas.options import PerPageLimit, Genre
from app.services.kinorium_playwright import KinoriumPlaywrightService
from app.services.kinorium_http import KinoriumHTTPService
from app.schemas.movies import MovieDetail
from app.core.http_client import http_client

router = APIRouter(prefix="/v1/kinorium", tags=["kinorium service"])

async def _run_kinorium_logic(movie_title: str, headless: bool, should_scrape: bool = True):
    kinorium = KinoriumPlaywrightService(headless=headless, should_scrape=should_scrape)
    result = await kinorium.movie_detail_executor(movie_title=movie_title)
    
    if not result:
        return {'status': 'error', 'message': 'No data found'}
    
    if isinstance(result, str):
        return {'status': 'OK', 'url': result}

    
    validated_result = MovieDetail(**result)
    return {'status': 'OK', 'data': validated_result}


@router.get("/health", status_code=status.HTTP_200_OK)
async def kinorium_health_check():
    """Health check endpoint for external service https://ua.kinorium.com/"""

    try:
        async with http_client.get("https://ua.kinorium.com") as response:
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
    """
    1️⃣ Простий запит (без браузера)
    Uses the aiohttp HTTP client to fetch data from kinorium by genre and pagination.
    
    """
    result = await KinoriumHTTPService().start_scraper(genre.id, page, per_page)

    return {"status": "OK", "data": result}


@router.post("/scraper/browser/headless", 
             status_code=status.HTTP_200_OK,
             summary="Scrape movie details (headless)")
async def kinorium_via_browser_headless(movie_title: str):
    """
    2️⃣ Headless-браузер (скрейпінг деталей фільму)
    
    Opens the browser in headless mode to scrape detailed movie information.

    Returns: Scraped movie details as a structured dictionary (Pydantic Model).
    """

    return await _run_kinorium_logic(movie_title=movie_title, headless=True, should_scrape=True)




@router.post(
        "/scraper/browser/debug", 
        status_code=status.HTTP_200_OK,
        summary="Scrape movie details (Debug/Visual)"
        )
async def kinorium_via_browser_debug(movie_title: str):
    """
    3️⃣ Браузер без headless (відкриття сторінки фільму)

    Opens the browser in non-headless mode for debugging purposes.
    
    Returns: URL of the movie detail page.

    """

    return await _run_kinorium_logic(movie_title=movie_title, headless=False, should_scrape=False)

