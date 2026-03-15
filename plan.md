# Website Monitor Bot — Implementation Plan

## Overview
A Telegram bot that monitors websites and alerts you instantly when they go down or come back up. Built with Python, deployed on your VPS.

---

## Stack
- `python-telegram-bot[job-queue]` — bot framework
- `aiohttp` — async HTTP requests for pinging sites
- `aiosqlite` — async SQLite for storing URLs
- `APScheduler` — scheduling the ping loop

Install everything:
```
pip install python-telegram-bot[job-queue] aiohttp aiosqlite apscheduler
```

---

## File Structure
```
monitor_bot/
├── main.py          # Entry point, starts the bot
├── bot.py           # All command handlers
├── checker.py       # Site ping logic
├── db.py            # SQLite operations
├── scheduler.py     # APScheduler setup
├── config.py        # BOT_TOKEN, CHECK_INTERVAL
└── requirements.txt
```

---

## Bot Commands
| Command | What it does |
|---|---|
| `/start` | Welcome message + instructions |
| `/add https://example.com` | Add a URL to monitor |
| `/remove https://example.com` | Remove a URL |
| `/status` | Show all URLs with up/down state and response time |
| `/interval 30` | Change check frequency in seconds |

---

## Database Schema (db.py)
Two tables only:

```sql
-- Stores which URLs each user is monitoring
CREATE TABLE IF NOT EXISTS sites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    chat_id INTEGER NOT NULL
);

-- Stores the last known state of each URL
CREATE TABLE IF NOT EXISTS state (
    url TEXT PRIMARY KEY,
    status TEXT,         -- 'up' or 'down'
    response_ms INTEGER,
    last_checked TEXT    -- ISO timestamp
);
```

---

## Core Logic (checker.py)
```python
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
```

---

## Alert Logic
This runs every X seconds via APScheduler. The key part is comparing old state vs new state:

```python
async def run_checks(bot):
    sites = await db.get_all_sites()  # list of {url, chat_id}

    for site in sites:
        result = await checker.check_site(site["url"])
        old_state = await db.get_state(site["url"])

        # Only alert if state changed
        if old_state and old_state["status"] != result["status"]:
            if result["status"] == "down":
                msg = f"🔴 DOWN: {site['url']}\nError: {result.get('error')}"
            else:
                msg = f"🟢 BACK UP: {site['url']}\nResponse: {result['ms']}ms"

            await bot.send_message(chat_id=site["chat_id"], text=msg)

        await db.update_state(site["url"], result)
```

---

## Build Phases

### Phase 1 — Commands working (Day 1)
- Set up bot with python-telegram-bot
- Implement `/start`, `/add`, `/remove`, `/status`
- Store URLs in memory (plain Python list for now, no DB yet)
- Test all commands work in Telegram

### Phase 2 — Checker working (Day 1-2)
- Write `checker.py` with the async ping function
- Test it manually — run it from terminal, print results
- Make sure it handles timeouts, connection errors, redirects

### Phase 3 — Scheduler loop (Day 2)
- Wire checker into APScheduler
- Run it every 60 seconds in the background
- Print results to console to verify it works
- Add the state comparison logic so it only alerts on changes

### Phase 4 — SQLite storage (Day 2)
- Write `db.py` with the two tables
- Replace in-memory list with DB calls
- Test that URLs survive a bot restart

### Phase 5 — Polish (Day 3)
- Add `/status` response with response times and last checked time
- Add `/interval` command to change check frequency
- Add error handling for invalid URLs in `/add`
- Clean up messages so they look good in Telegram

### Phase 6 — Deploy on VPS (Day 3)
- Copy project to your Vultr VPS
- Create a systemd service so it auto-starts and restarts on crash
- Run it live for a few hours and verify alerts work
- Record a demo GIF: add a site, kill the site, show the alert arriving

---

## Systemd Service (deploy on VPS)
Create `/etc/systemd/system/monitor_bot.service`:

```ini
[Unit]
Description=Website Monitor Telegram Bot
After=network.target

[Service]
User=root
WorkingDirectory=/root/monitor_bot
ExecStart=/usr/bin/python3 main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Then run:
```bash
systemctl daemon-reload
systemctl enable monitor_bot
systemctl start monitor_bot
systemctl status monitor_bot
```

---

## config.py
```python
BOT_TOKEN = "your_token_here"
CHECK_INTERVAL = 60  # seconds
DB_PATH = "monitor.db"
```

---

## Gig Demo Checklist
Before posting the gig, make sure you have:
- [ ] Bot running live on VPS 24/7
- [ ] GIF showing: add URL → site goes down → alert arrives in Telegram
- [ ] `/status` screenshot showing multiple sites being monitored
- [ ] GitHub repo with clean README and setup instructions

---

## Estimated Timeline
| Day | Goal |
|---|---|
| Day 1 | Phase 1 + Phase 2 done |
| Day 2 | Phase 3 + Phase 4 done |
| Day 3 | Phase 5 + Phase 6 done, gig live |