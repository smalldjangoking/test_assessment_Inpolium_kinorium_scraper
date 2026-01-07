import asyncio
import logging
from app.core.browser import browser_manager

class KinoriumPlaywrightService:
    def __init__(self, headless: bool = True, should_scrape: bool = True) -> None:
        self.headless = headless
        self.should_scrape = should_scrape
        self._manager = browser_manager

    async def movie_detail_executor(self, movie_title: str):
        """Executes the Playwright browser to scrape movie details from ua.kinorium.com
           if should_scrape is True.
        """

        browser = await self._manager.get_browser(headless=self.headless)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            #Method to find and navigate to movie detail page
            page = await self._find_and_navigate(movie_title=movie_title, page=page)

            if not page:
                return None
            if not self.should_scrape:
                return page.url

            #Method to scrape movie details from the detail page


        except Exception as e:
            logging.error(f"Error during Playwright scraping: {e}")

        finally:
            if not self.headless:
                await asyncio.sleep(5)  # Pause to observe the browser in non-headless mode
            await context.close()

    async def _find_and_navigate(self, movie_title: str, page):
        """Finds the movie by title and navigates to its detail page if found"""
        await page.goto(f"https://ua.kinorium.com/search/?q={movie_title}", wait_until="load")
        
        movie_locator = page.locator(".movieList .item").first
        
        if await movie_locator.count() == 0:
            logging.info(f"Фильм {movie_title} не найден.")
            return None
        
        await movie_locator.locator(".search-page__title-link").click()
        await page.wait_for_load_state("domcontentloaded")
        return page
    
    async def _scrape_movie_details(self, page):
        """Scrapes movie details from the current page"""

        

            


   