from telegram import Update
from telegram.ext import ContextTypes
from . import db
from . import config

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 Welcome to the Website Monitor Bot!\n\n"
        "I can monitor your websites and alert you when they go down.\n\n"
        "Commands:\n"
        "/add <url> - Add a URL to monitor\n"
        "/remove <url> - Remove a URL\n"
        "/status - Show all your URLs status\n"
        "/interval <seconds> - Change check frequency"
    )
    await update.message.reply_text(welcome_text)

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /add <url>")
        return

    url = context.args[0]
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    chat_id = update.effective_chat.id
    await db.add_site(url, chat_id)
    await update.message.reply_text(f"✅ Added {url} to your monitor list.")

async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /remove <url>")
        return

    url = context.args[0]
    chat_id = update.effective_chat.id
    await db.remove_site(url, chat_id)
    await update.message.reply_text(f"🗑️ Removed {url} from your monitor list.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    sites = await db.get_user_sites(chat_id)

    if not sites:
        await update.message.reply_text("You are not monitoring any websites yet. Use /add <url> to start.")
        return

    report = "📊 Website Status Report:\n\n"
    for site in sites:
        url = site['url']
        state = await db.get_state(url)
        if state:
            icon = "🟢" if state['status'] == 'up' else "🔴"
            ms = f"{state['response_ms']}ms" if state['response_ms'] else "N/A"
            report += f"{icon} {url}\n   Status: {state['status'].upper()}\n   Response: {ms}\n   Last Check: {state['last_checked']}\n\n"
        else:
            report += f"⚪ {url}\n   Status: PENDING FIRST CHECK\n\n"

    await update.message.reply_text(report)

async def interval(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(f"Current interval: {config.CHECK_INTERVAL}s\nUsage: /interval <seconds>")
        return

    try:
        new_interval = int(context.args[0])
        if new_interval < 10:
             await update.message.reply_text("Minimum interval is 10 seconds.")
             return
        
        config.CHECK_INTERVAL = new_interval
        
        # Reschedule the job
        job_queue = context.application.job_queue
        current_jobs = job_queue.get_jobs_by_name('site_checker')
        for job in current_jobs:
            job.schedule_removal()
        
        from . import scheduler
        job_queue.run_repeating(scheduler.run_checks, interval=new_interval, first=new_interval, name='site_checker')

        await update.message.reply_text(f"✅ Check interval updated to {new_interval}s and rescheduled.")
    except ValueError:
        await update.message.reply_text("Please provide a valid number of seconds.")
