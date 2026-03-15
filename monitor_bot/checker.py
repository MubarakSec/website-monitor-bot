import aiohttp
import time

async def check_site(url: str) -> dict:
    start = time.monotonic()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                timeout=aiohttp.ClientTimeout(total=10),
                allow_redirects=True
            ) as response:
                ms = int((time.monotonic() - start) * 1000)
                return {
                    "url": url,
                    "status": "up",
                    "code": response.status,
                    "ms": ms
                }
    except Exception as e:
        return {
            "url": url,
            "status": "down",
            "code": None,
            "ms": None,
            "error": str(e)
        }
