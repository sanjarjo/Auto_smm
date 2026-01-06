# app.py
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from config import BOT_TOKEN  # Token config.py dan

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Salom! Bot ishga tushdi.")

# Telegram botni ishga tushirish
application = ApplicationBuilder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))

print("Bot ishga tushmoqda...")

# Termux va boshqa interactive muhitlar uchun
loop = asyncio.get_event_loop()
loop.create_task(application.run_polling(drop_pending_updates=True))
loop.run_forever()
