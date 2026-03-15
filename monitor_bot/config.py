import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_token_here")
CHECK_INTERVAL = 60  # seconds
DB_PATH = "monitor.db"
