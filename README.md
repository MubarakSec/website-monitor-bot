<h1 align="center">
  Website Monitor Bot
</h1>

<p align="center">
  <strong>A fast, asynchronous Telegram bot that monitors websites and alerts you instantly when they go down or come back up.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/python--telegram--bot-v20+-blue.svg" alt="PTB Version">
  <img src="https://img.shields.io/badge/Database-SQLite-lightgrey.svg" alt="Database">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
</p>

## 📌 Features

- **Real-time Monitoring:** Continuously checks your websites at customizable intervals.
- **Instant Alerts:** Get notified directly on Telegram the moment a site goes down or comes back online.
- **Asynchronous & Fast:** Built with `aiohttp` and `python-telegram-bot` for high concurrency and performance.
- **Persistent Storage:** Safely stores your monitored URLs and their statuses using `aiosqlite`.
- **User-Friendly Commands:** Manage your monitoring list directly from Telegram.

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8 or higher.
- A Telegram Bot Token from [@BotFather](https://t.me/botfather).

### 2. Installation
Clone the repository and install the required dependencies:
```bash
git clone https://github.com/MubarakSec/website-monitor-bot.git
cd website-monitor-bot
pip install -r monitor_bot/requirements.txt
```

### 3. Configuration
Copy the example environment file and add your Telegram Bot Token:
```bash
cp .env.example .env
```
Edit the `.env` file:
```env
BOT_TOKEN=your_telegram_bot_token_here
```

### 4. Running the Bot
Start the bot using the provided runner script:
```bash
python3 run.py
```

## 💬 Bot Commands

Manage your bot directly from Telegram with these commands:

| Command | Description |
|---------|-------------|
| `/start` | Display the welcome message and instructions. |
| `/add <url>` | Add a new website to your monitoring list. |
| `/remove <url>` | Remove a website from your monitoring list. |
| `/status` | View the current status and response times of all your monitored websites. |
| `/interval <sec>` | Adjust the frequency of website checks (minimum 10 seconds). |

## 🛠️ Deployment (VPS)

To keep your bot running 24/7, deploy it on a VPS using `systemd`.

1. **Copy the repository** to your server.
2. **Edit the `monitor_bot.service` file**, ensuring the `WorkingDirectory` matches your absolute project path.
3. **Move the service file** to the systemd directory:
   ```bash
   sudo mv monitor_bot.service /etc/systemd/system/
   ```
4. **Enable and start the service:**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable monitor_bot
   sudo systemctl start monitor_bot
   ```
5. **Check the status:**
   ```bash
   sudo systemctl status monitor_bot
   ```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
