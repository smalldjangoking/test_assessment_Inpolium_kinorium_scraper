import aiohttp
from typing import AsyncContextManager

class HTTPClient:
    """A singleton HTTP client using aiohttp.ClientSession for the entire project."""

    def __init__(self):
        self._session: aiohttp.ClientSession | None = None

    def start(self):
        """Creates ClientSession for aiohttp for full project"""
        if self._session is not None:
            return
        
        self._session = aiohttp.ClientSession()

    async def stop(self):
        """Closes ClientSession for aiohttp for full project"""
        if self._session:
            await self._session.close()
            self._session = None

    def get(self, url: str, **kwargs) -> AsyncContextManager[aiohttp.ClientResponse]:
        """Performs a GET request using the aiohttp ClientSession"""
        if self._session is None:
            raise RuntimeError("HTTPClient session is not started.")
        
        return self._session.get(url, **kwargs)

    
http_client = HTTPClient()