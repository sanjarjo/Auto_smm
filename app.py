import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

from config import BOT_TOKEN, ADMIN_ID
from notifier import init_notifier
from scheduler import scheduler_loop

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Salom! Bot ishga tushdi!")

async def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    # notifier init
    init_notifier(application, ADMIN_ID)

    # background scheduler
    application.create_task(scheduler_loop())

    print("🤖 Bot to‘liq ishga tushdi...")
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
