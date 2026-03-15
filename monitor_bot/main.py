import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler
from . import bot as bot_handlers
from . import db
from . import config
from . import scheduler

async def main():
    # Initialize DB
    await db.init_db()

    # Create application
    application = ApplicationBuilder().token(config.BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", bot_handlers.start))
    application.add_handler(CommandHandler("add", bot_handlers.add))
    application.add_handler(CommandHandler("remove", bot_handlers.remove))
    application.add_handler(CommandHandler("status", bot_handlers.status))
    application.add_handler(CommandHandler("interval", bot_handlers.interval))

    # Schedule checks
    job_queue = application.job_queue
    job_queue.run_repeating(scheduler.run_checks, interval=config.CHECK_INTERVAL, first=10, name='site_checker')

    # Start bot
    print("Bot is starting...")
    await application.run_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
