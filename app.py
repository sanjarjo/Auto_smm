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


# Background scheduler
async def scheduler_loop():
    while True:
        await ensure_orders()
        await check_orders()
        await asyncio.sleep(60)


# Application start bo‘lganda chaqiriladi
async def post_init(application):
    # notifier
    init_notifier(application, ADMIN_ID)

    # background task
    application.create_task(scheduler_loop())


def main():
    application = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    application.add_handler(CommandHandler("start", start))

    print("🤖 Bot to‘liq ishga tushdi...")
    application.run_polling()


if __name__ == "__main__":
    main()
