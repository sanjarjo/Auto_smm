# app.py
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from config import BOT_TOKEN, ADMIN_ID, CHECK_INTERVAL
from scheduler import ensure_orders, check_orders
from notifier import init_notifier


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


async def post_init(application):
    loop = asyncio.get_running_loop()
    init_notifier(application, loop, ADMIN_ID)
    asyncio.create_task(scheduler_loop())


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


if __name__ == "__main__":
    asyncio.run(main())
