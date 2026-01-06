# app.py
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

from config import BOT_TOKEN, ADMIN_ID, CHECK_INTERVAL
from scheduler import ensure_orders, check_orders
from notifier import init_notifier


# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Salom! Bot ishga tushdi!")


# Background task
async def scheduler_job(context: ContextTypes.DEFAULT_TYPE):
    ensure_orders()
    check_orders()


async def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # notifier ni ulash
    init_notifier(
        application=application,
        event_loop=asyncio.get_running_loop(),
        admin_id=ADMIN_ID
    )

    application.add_handler(CommandHandler("start", start))

    # JobQueue — HAR 60 SONIYA
    application.job_queue.run_repeating(
        scheduler_job,
        interval=CHECK_INTERVAL,
        first=5
    )

    print("🤖 Bot to‘liq ishga tushdi...")
    await application.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
