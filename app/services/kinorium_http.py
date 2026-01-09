from app.core.http_client import http_client
from bs4 import BeautifulSoup
import logging


class KinoriumHTTPService:
    """
    Service for scraping movie details from Kinorium using HTTP client.

    This service handles the complete scraping workflow:
        1. Finds movies by genre
        2. scraps movie details which are visible

    Attributes: 
        http_client:  Instance of the HTTPClient

    Returns:
        list[dict]: Movie details
    """
    def __init__(self) -> None:
        self.http_client = http_client

    async def start_scraper(self, genre_id: int, page: int, per_page: int) -> list:
        """
        Main method to execute the HTTP scraping process for a movie details page

        Args:
            genre_id (int): ID of the genre to filter movies.
            page (int): Current page number for pagination. (Optional)
            per_page (int): Number of movies to display per page. (Optional)

        Returns:
            list[dict]: A list of dictionaries containing movie details
        """
        #Fething Data by genre, per_page and page number
        html_result = await self._fetch_data(genre_id, page, per_page)
        #returns scraped movie details
        return self._scrap_movie_details(html_result)



    def _scrap_movie_details(self, html: str) -> list:
        """
        Parses raw HTML content to extract movie information.
        
        Params: 
            html (str): Accepts a html file to scrap in
        Retuns:
            list[dict]: A list of dictionaries containing movie details
        """
        soup = BeautifulSoup(html, "lxml")
        movies = soup.select('div.item')
        results = []

        for movie in movies:
            poster = movie.select_one('.movie-list-poster')
            title = movie.select_one('.movie-title__text span')
            title_eng = None
            year = None
            genres = []
            duration = None
            clean_poster = None


            #raw
            title_eng_and_year = movie.select_one('.filmList__small-text')
            genres_duration = movie.select_one('.filmList__extra-info')

            if title_eng_and_year:
                #splits title_english variant and year of the movie
                full_text = title_eng_and_year.get_text(strip=True).split('(')[0].split(',')
                title_eng = full_text[0].strip()
                year = full_text[-1].strip()

            if genres_duration:
                # split genres and duration
                full_text = genres_duration.find(string=True)

                if full_text:
                    full_text = full_text.split(',')
                    genres = [g.strip() for g in full_text[:-1]]
                    duration = " ".join(full_text[-1].split())

            if poster:
                # cleans the poster link
                raw_poster = str(poster.get('src', ''))
                clean_poster = raw_poster.split('?')[0]

            results.append({
                'title': title.get_text(strip=True) if title else None,
                'title_eng': title_eng if title_eng else None,
                'year': year if year else None,
                'genres': genres if genres else [],
                'duration': duration if duration else None,
                'poster': clean_poster if clean_poster else None
            })
        return results


    async def _fetch_data(self, genre_id: int, page: int, per_page: int) -> str:
        """
        Sends an asynchronous GET request to the Kinorium handler
        
        Args:
            genre_id (int): ID of the genre to filter movies.
            page (int): Current page number for pagination. (Optional)
            per_page (int): Number of movies to display per page. (Optional)

        Returns:
            str: The HTML content extracted from the JSON response or an empty string.    
        """
        url = "https://ua.kinorium.com/handlers/filmList/"

        #(обязательно проверь актуальность 'session')
        cookies = {
            "session": "1u2j4mf7a3i0i3d9h83rfb8a44",
            "x119": "88513",
            "PHPSESSID": "pj95efe3eommbikt25idka2osn"
        }

        # 3. Заголовки, чтобы запрос выглядел как от твоего браузера
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://ua.kinorium.com/R2D2/"
        }

        # 4. query params
        params = {
            "type": "R2D2",
            "order": "rating",
            "page": str(page),
            "perpage": str(per_page),
            "genres[]": str(genre_id),
            "list_only": "1",
            "ajax": "list"
        }

        
        async with self.http_client.get(
            url, 
            params=params, 
            headers=headers, 
            cookies=cookies
        ) as response:
            if response.status == 200:
                data = await response.json()
                result = data.get("result", {})
                if isinstance(result, dict):
                    return result.get("html", "")
            logging.warning('The HTML response is empty.')
            return ""
