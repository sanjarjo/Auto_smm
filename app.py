# app.py

import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

from config import BOT_TOKEN, ADMIN_ID
from scheduler import ensure_orders, check_orders
from notifier import init_notifier


# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Salom! Bot ishga tushdi!")


# Background scheduler (JobQueue o‘rniga)
async def scheduler_loop():
    while True:
        try:
            await ensure_orders()
            await check_orders()
        except Exception as e:
            print("Scheduler error:", e)

        await asyncio.sleep(60)


def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))

    # Notifier
    init_notifier(application, ADMIN_ID)

    # Background task — TO‘G‘RI JOYDA
    application.post_init = lambda app: app.create_task(scheduler_loop())

    print("🤖 Bot to‘liq ishga tushdi...")
    application.run_polling()


if __name__ == "__main__":
    main()
