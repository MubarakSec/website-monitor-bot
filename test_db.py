import asyncio
from monitor_bot import db, config
config.DB_PATH = "test_monitor.db"

async def test():
    await db.init_db()
    await db.add_site("https://example.com", 12345)
    sites = await db.get_all_sites()
    print("Sites:", sites)
    await db.update_state("https://example.com", {"status": "up", "ms": 42})
    state = await db.get_state("https://example.com")
    print("State:", dict(state))
    await db.remove_site("https://example.com", 12345)

asyncio.run(test())
