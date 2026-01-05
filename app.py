# app.py
import asyncio
from telegram.ext import Application
from config import BOT_TOKEN, ADMIN_ID, CHECK_INTERVAL
from scheduler import check_orders, ensure_orders
from notifier import init_notifier

# 🔹 Async event loop
loop = asyncio.get_event_loop()

# 🔹 Telegram bot
tg_app = Application.builder().token(BOT_TOKEN).build()

# 🔹 Notifier init
init_notifier(tg_app, loop, ADMIN_ID)

async def background_loop():
    """Background scheduler loop"""
    ensure_orders()
    while True:
        check_orders()
        await asyncio.sleep(CHECK_INTERVAL)

async def main():
    # 🔹 Start polling
    await tg_app.initialize()
    await tg_app.start_polling()
    
    # 🔹 Start background scheduler
    loop.create_task(background_loop())

    # 🔹 Idle bot (keep running)
    await tg_app.idle()

if __name__ == "__main__":
    loop.run_until_complete(main())
