import asyncio
from monitor_bot import checker

async def test():
    result = await checker.check_site("https://www.google.com")
    print(result)
    result_fail = await checker.check_site("https://this-site-should-not-exist-ever-123.com")
    print(result_fail)

asyncio.run(test())
