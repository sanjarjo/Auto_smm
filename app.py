# app.py
import nest_asyncio
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Tokenni config.py dan import qilamiz
from config import BOT_TOKEN

# nest_asyncio bilan mavjud event loop ustida ishlashga ruxsat beramiz
nest_asyncio.apply()

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Salom! Bot ishga tushdi!")

async def main():
    # Botni yaratish
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handler qo‘shish
    application.add_handler(CommandHandler("start", start))

    # Pollingni ishga tushirish
    print("Bot ishga tushmoqda...")
    await application.run_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\nBot to‘xtatildi.")
