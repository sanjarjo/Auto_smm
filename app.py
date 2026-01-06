# app.py

import nest_asyncio
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from config import BOT_TOKEN, ADMIN_ID
from database import save_order, update_status, get_active_orders, has_active
from scheduler import ensure_orders, check_orders
from notifier import init_notifier

nest_asyncio.apply()

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Salom! Bot ishga tushdi!")

# Bu background loop
async def scheduler_loop(application):
    while True:
        await ensure_orders()   # async funksiya
        await check_orders()    # async funksiya
        await asyncio.sleep(60) # 60 soniya kutish

async def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))

    # Notifier-ni ishga tushirish
    init_notifier(application, ADMIN_ID)

    # Background scheduler
    application.create_task(scheduler_loop(application))

    print("🤖 Bot to‘liq ishga tushdi...")
    await application.run_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\nBot to‘xtatildi.")
