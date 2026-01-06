import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import BOT_TOKEN

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Bot ishga tushdi ✅")

async def main():
    # Botni yaratish
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Handler qo‘shish
    application.add_handler(CommandHandler("start", start))
    
    # Botni polling orqali ishga tushirish
    print("Bot ishga tushdi. Ctrl+C bilan to‘xtating.")
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
