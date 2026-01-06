# app.py
import nest_asyncio
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from config import BOT_TOKEN, ADMIN_ID, CHECK_INTERVAL
from scheduler import ensure_orders, check_orders
from notifier import init_notifier

# nest_asyncio bilan Termux yoki boshqa existing event loop ustida ishlashga ruxsat
nest_asyncio.apply()

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Salom! Bot ishga tushdi!")

# Background task: SMM zakazlarini tekshirish va qo'shish
async def background_loop(application):
    while True:
        try:
            ensure_orders()   # yangi zakazlarni qo'shish
            check_orders()    # mavjud zakazlarni tekshirish
        except Exception as e:
            print("Background loop error:", e)
        await asyncio.sleep(CHECK_INTERVAL)

async def main():
    # Botni yaratish
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    # Notifierni init qilish
    init_notifier(application, asyncio.get_event_loop(), ADMIN_ID)

    # Background loopni ishga tushirish
    asyncio.create_task(background_loop(application))

    print("Bot ishga tushmoqda...")
    await application.run_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\nBot to‘xtatildi.")
