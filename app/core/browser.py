import asyncio
from playwright.async_api import async_playwright, Browser, Playwright

class BrowserManager():
    """Playwright browser manager for controlling singleton instances of headless and headless false"""
    _instance = None
    _playwright: Playwright | None = None
    _headless_browser: Browser | None = None
    _visible_browser: Browser | None = None
    _lock = asyncio.Lock()


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    async def get_browser(self, headless: bool = True) -> Browser:
        """Returns a singleton browser instance based on headless parameter"""

        async with self._lock:
            if self._playwright is None:
                self._playwright = await async_playwright().start()
            
            if headless:
                if self._headless_browser is None:
                    self._headless_browser = await self._playwright.chromium.launch(headless=True)
                return self._headless_browser
            else:
                if self._visible_browser is None:
                    self._visible_browser = await self._playwright.chromium.launch(headless=False)
                return self._visible_browser
            
    async def stop_engine(self) -> None:
        """Closes all browser instances and stops playwright"""
        async with self._lock:
            if self._headless_browser:
                await self._headless_browser.close()
                self._headless_browser = None
            
            if self._visible_browser:
                await self._visible_browser.close()
                self._visible_browser = None
            
            if self._playwright:
                await self._playwright.stop()
                self._playwright = None

browser_manager = BrowserManager()