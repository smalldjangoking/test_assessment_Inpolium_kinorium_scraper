from app.core.http_client import http_client


class KinoriumHTTPService:
    """
    Service for scraping movie details from Kinorium using HTTP client.
    something to write here
    """

    async def start_scraper(self, genre_id: int, page: int, per_page: int):
        """Starts the Kinorium scraper using HTTP client"""
        html_result = await self._fetch_data(genre_id, page, per_page)
        pass



    def _scrap_movie_details(self):
        pass


    async def _fetch_data(self, genre_id: int, page: int, per_page: int):
        async with http_client.get(
            "https://ua.kinorium.com/R2D2/",
            params={"genres[]": genre_id, 
                    "page": page, 
                    "per_page": per_page
                   }) as response:
            return await response.text()    
