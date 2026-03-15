import aiosqlite
import datetime
from .config import DB_PATH

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS sites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                chat_id INTEGER NOT NULL
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS state (
                url TEXT PRIMARY KEY,
                status TEXT,         -- 'up' or 'down'
                response_ms INTEGER,
                last_checked TEXT    -- ISO timestamp
            )
        ''')
        await db.commit()

async def add_site(url: str, chat_id: int) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('SELECT id FROM sites WHERE url = ? AND chat_id = ?', (url, chat_id)) as cursor:
            if await cursor.fetchone():
                return False
        await db.execute('INSERT INTO sites (url, chat_id) VALUES (?, ?)', (url, chat_id))
        await db.commit()
        return True

async def remove_site(url: str, chat_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('DELETE FROM sites WHERE url = ? AND chat_id = ?', (url, chat_id))
        await db.commit()

async def get_all_sites():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('SELECT url, chat_id FROM sites') as cursor:
            return [dict(row) for row in await cursor.fetchall()]

async def get_user_sites(chat_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('SELECT url FROM sites WHERE chat_id = ?', (chat_id,)) as cursor:
            return [dict(row) for row in await cursor.fetchall()]

async def get_state(url: str):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('SELECT * FROM state WHERE url = ?', (url,)) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None

async def update_state(url: str, result: dict):
    async with aiosqlite.connect(DB_PATH) as db:
        now = datetime.datetime.now().isoformat()
        await db.execute('''
            INSERT OR REPLACE INTO state (url, status, response_ms, last_checked)
            VALUES (?, ?, ?, ?)
        ''', (url, result['status'], result['ms'], now))
        await db.commit()
