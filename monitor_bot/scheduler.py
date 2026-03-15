from telegram.ext import ContextTypes
from . import db
from . import checker

async def run_checks(context: ContextTypes.DEFAULT_TYPE):
    bot = context.bot
    sites = await db.get_all_sites()  # list of {url, chat_id}

    if not sites:
        return

    # 1. Collect unique URLs
    unique_urls = set(site['url'] for site in sites)
    
    # 2. Get current state from DB for all unique URLs
    old_states = {}
    for url in unique_urls:
        old_states[url] = await db.get_state(url)

    # 3. Perform checks
    new_results = {}
    for url in unique_urls:
        new_results[url] = await checker.check_site(url)

    # 4. Alert users if state changed
    for site in sites:
        url = site["url"]
        result = new_results[url]
        old_state = old_states[url]

        # Only alert if state changed
        if old_state and old_state["status"] != result["status"]:
            if result["status"] == "down":
                msg = f"🔴 DOWN: {url}\nError: {result.get('error')}"
            else:
                msg = f"🟢 BACK UP: {url}\nResponse: {result['ms']}ms"

            try:
                await bot.send_message(chat_id=site["chat_id"], text=msg)
            except Exception as e:
                print(f"Error sending alert to {site['chat_id']}: {e}")

    # 5. Update DB with new results
    for url, result in new_results.items():
        await db.update_state(url, result)
