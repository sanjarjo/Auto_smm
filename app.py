# app.py
import asyncio
import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from config import BOT_TOKEN, ADMIN_ID, CHECK_INTERVAL
from scheduler import ensure_orders, check_orders
from notifier import init_notifier

# nest_asyncio bilan mavjud event loop ustida ishlashga ruxsat beramiz
nest_asyncio.apply()

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Salom! Bot ishga tushdi!")

# Background scheduler
async def scheduler_loop(application):
    while True:
        try:
            # ensure_orders va check_orders sync bo'lgani uchun to_thread ishlatamiz
            await asyncio.to_thread(ensure_orders)
            await asyncio.to_thread(check_orders)
            await ensure_orders()  # await qo'shildi
        await check_orders()   # await qo'shildi
        except Exception as e:
            print("Scheduler xatosi:", e)
        await asyncio.sleep(60)

async def main():
    # Botni yaratish
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # /start handler qo‘shish
    application.add_handler(CommandHandler("start", start))

    # Notifier-ni ishga tushirish
    init_notifier(application, ADMIN_ID)

    # Background scheduler task
    application.create_task(scheduler_loop(application))

    # Botni ishga tushirish (polling)
    print("🤖 Bot to‘liq ishga tushdi...")
    await application.run_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\nBot to‘xtatildi.")
