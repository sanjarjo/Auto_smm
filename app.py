# app.py
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from config import BOT_TOKEN, ADMIN_ID, CHECK_INTERVAL
from scheduler import ensure_orders, check_orders
from notifier import init_notifier


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Salom! Bot ishga tushdi!")


async def background_scheduler(app):
    while True:
        try:
            ensure_orders()
            check_orders()
        except Exception as e:
            print("Scheduler xato:", e)
        await asyncio.sleep(CHECK_INTERVAL)


def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    init_notifier(
        application=application,
        event_loop=asyncio.get_event_loop(),
        admin_id=ADMIN_ID
    )

    application.add_handler(CommandHandler("start", start))

    # background task
    application.create_task(background_scheduler(application))

    print("🤖 Bot to‘liq ishga tushdi (event loop xatosiz)")
    application.run_polling()


if __name__ == "__main__":
    main()
