# app.py
import nest_asyncio
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from config import BOT_TOKEN, ADMIN_ID, CHECK_INTERVAL
from scheduler import ensure_orders, check_orders
from notifier import init_notifier

# Termux / nested event loop muammosi uchun
nest_asyncio.apply()

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot ishlayapti!")

# Background scheduler
async def scheduler_loop():
    while True:
        try:
            await asyncio.to_thread(ensure_orders)
            await asyncio.to_thread(check_orders)
        except Exception as e:
            print("Scheduler error:", e)
        await asyncio.sleep(CHECK_INTERVAL)

# post_init chaqiriladi bot run bo‘lganida
async def post_init(application):
    loop = asyncio.get_running_loop()
    init_notifier(application, loop, ADMIN_ID)
    asyncio.create_task(scheduler_loop())

# Main
async def main():
    application = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    print("🤖 Bot to‘liq ishga tushdi...")
    await application.run_polling()

# Termux / nested loop uchun oddiy start
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
