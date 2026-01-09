import asyncio
import logging
from app.core.browser import browser_manager
from playwright.async_api import Page

class KinoriumPlaywrightService:
    """
    Service for scraping movie details from Kinorium using Playwright.

    This service handles the complete scraping workflow:
    1. Finds a movie by title.
    2. Navigates to the movie detail page.
    3. Scrapes comprehensive movie details.

    Attributes:
        headless (bool): Whether to run the browser in headless mode.
        should_scrape (bool): Whether to scrape details or just return the URL.
        _manager: Instance of the browser manager for context and page handling.

    """

    def __init__(self, headless: bool = True, should_scrape: bool = True) -> None:
        self.headless = headless
        self.should_scrape = should_scrape
        self._manager = browser_manager

    async def movie_detail_executor(self, movie_title: str) -> dict | str | None:
        """
        Main method to execute the Playwright scraping process for a movie detail page

        Args:
            movie_title (str): The name of the movie to search for.

        Returns:
            dict: Movie details if should_scrape is True.
            str: URL of the movie detail page if should_scrape is False.
            None: If the movie is not found or an error occurs.
        """

        browser = await self._manager.get_browser(headless=self.headless)
        # Set up browser context with Ukrainian locale and Kyiv timezone
        context = await browser.new_context(
            locale="uk-UA",
            timezone_id="Europe/Kyiv",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
            )
        page = await context.new_page()

        try:
            #Method to find and navigate to movie detail page
            page = await self._find_and_navigate(movie_title=movie_title, page=page)

            if not page:
                return None
            if not self.should_scrape:
                return page.url

            #Method to scrape movie details from the detail page

            return await self._scrape_movie_details(page=page)


        except Exception as e:
            logging.error(f"Error during Playwright scraping: {e}")

        finally:
            if not self.headless:
                await asyncio.sleep(5)  # Pause to observe the browser in non-headless mode
            await context.close()

    async def _find_and_navigate(self, movie_title: str, page) -> Page | None:
        """
        Help Method: Finds the movie by title and navigates to its detail page if found
        
        Args:
            movie_title (str): The name of the movie to search for.
            page: Playwright page object.
        
        Returns:
            Page: Playwright page object of the movie detail page.
            None: If the movie is not found.
        """

        await page.goto(f"https://ua.kinorium.com/search/?q={movie_title}", wait_until="load")
        movie_locator = page.locator(".movieList .item").first
        
        if await movie_locator.count() == 0:
            logging.info(f"Movie {movie_title} is not found.")
            return None
        
        await movie_locator.locator(".search-page__title-link").click()
        await page.wait_for_load_state("load", timeout=1000)
        return page
    
    async def _scrape_movie_details(self, page) -> dict:
        """
        Scrapes comprehensive movie details.

        Extracts basic info (title, year, etc.), production details, 
        ratings from multiple platforms, and the full production crew list from /cast/.

        Args:
            page: Playwright page object of the movie detail page.

        Returns:
                dict: A structured dictionary containing:
                        - url (str): Scraped page URL.
                        - title (str): Movie title.
                        - description (str): Plot summary.
                        - year (str): Release year.
                        - country (list[str]): Country of origin.
                        - duration (str): Runtime.
                        - budget (str): Financial info.
                        - poster (str): URL to the movie poster.
                        - age_restriction (str): Content rating (e.g., '16').
                        - logline (str): Tagline or slogan.
                        - production_companies (list[str]): Names of studios.
                        - genres (list[str]): List of movie genres.
                        - ratings (list[dict]): Platform ratings (platform name and value).
                        - crew (list[dict]): All production crew grouped by role.
        """

        # -- Helper locators and counts --
        age_restriction = await page.locator('.film-page__mkrf-box-icon').get_attribute('class')
        age_restriction = age_restriction.split('-')[-1] if age_restriction else 'N/A'

        production_companies = page.locator('.film-page__company a')
        count_production_companies = await production_companies.count()

        genres = page.locator('li[itemprop="genre"]')
        count_genres = await genres.count()
        
        ratings_container = page.locator('ul.ratingsBlock')
        ratings_elements = ratings_container.locator('li')
        count_ratings = await ratings_elements.count()

        country = page.locator('a[itemprop="countryOfOrigin"]')
        count_country = await country.count()

        # -- Scraping data --
        page_detail_url = page.url
        title = await page.locator(".film-page__title-text").inner_text()
        description = await page.locator('section[itemprop="description"]').inner_text()
        year = await page.locator('.film-page__date a').inner_text()
        duration = await page.locator('.infotable tbody tr').nth(2).locator('td.data').inner_text()
        budget = await page.locator('.box-budget-tooltip').inner_text()
        poster = await page.locator('.movie_gallery_poster').get_attribute('src')
        poster = poster.split('?')[0]
        logline = await page.locator('.film-page__slogan span').nth(1).text_content()
        production_companies = [await production_companies.nth(i).inner_text() for i in range(count_production_companies)]
        genres = [await genres.nth(i).text_content() for i in range(count_genres)]
        country = [await country.nth(i).inner_text() for i in range(count_country)]

        # -- Getting ratings of the movie --
        ratings_list = [] #list of platform ratings
        for i in range(count_ratings):
            platform = await ratings_elements.nth(i).locator('a').evaluate(
            "node => node.childNodes[0].textContent.trim()")
            rating = await ratings_elements.nth(i).locator('a span.value').inner_text()
            ratings_list.append({'platform': platform, 'rating': rating if rating else None})


        # -- Getting crew information --
        await page.locator('h2.headlines-slide_crew a[href*="/cast/"]').first.click() #goes to /cast/ page of movie
        await page.wait_for_load_state("load", timeout=10000)
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        crew_table = page.locator('.personList > div')
        count_crew_table = await crew_table.count()

        crew = [] #list of role groups
        for i in range(count_crew_table):
            role_table = crew_table.nth(i)
            role_title = await role_table.locator('.cast-page__title').inner_text()
            role_crew = role_table.locator('.crew-wrap div.filterData')
            count_role_crew = await role_crew.count()

            people_in_this_role = [] #people belonging to role group
            for r in range(count_role_crew):
                person_table = role_crew.nth(r)

                name = await person_table.locator('.cast-page__item-name').inner_text()
                #Image
                img_element = person_table.locator('img.cast-page__item-img_person, img.cast-page__item-img').first
                image = await img_element.get_attribute('src')
                if not image:
                    image = await person_table.locator('link[itemprop="image"]').get_attribute('content')
                clear_image_url = image.split('?')[0] if image else None

                person_dict = {
                    'name': name,
                    'image': clear_image_url
                }
                people_in_this_role.append(person_dict)

            crew.append({
                'role': role_title,
                'people': people_in_this_role
            })

        return {
        'url': page_detail_url,
        'title': title,
        'description': description,
        'year': year,
        'country': country,
        'duration': duration,
        'budget': budget,
        'poster': poster,
        'age_restriction': age_restriction,
        'logline': logline,
        'production_companies': production_companies,
        'genres': genres,
        'ratings': ratings_list,
        'crew': crew
    }    


   