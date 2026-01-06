import os
import asyncio
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler
from config import BOT_TOKEN  # Tokenni import qilamiz

app = Flask(__name__)

# Telegram bot start komandasi
async def start(update, context):
    await update.message.reply_text("Salom! Bot ishga tushdi.")

# Telegram botni ishga tushirish
application = ApplicationBuilder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))

# Flask server route
@app.route("/")
def index():
    return "Bot is running!"

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    
    # Telegram pollingni background-da ishga tushirish
    loop.create_task(application.run_polling(drop_pending_updates=True))
    
    # Flask serverni ishga tushirish
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
