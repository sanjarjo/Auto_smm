import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio

from config import BOT_TOKEN  # config.py ichida: BOT_TOKEN = "YOUR_BOT_TOKEN"

app = Flask(__name__)

# Telegram /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Salom! Bot webhook orqali ishlayapti.")

# Botni ishga tushiramiz
application = ApplicationBuilder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))

# Webhook route
@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
def webhook():
    """Telegram POST requestlarini qabul qiladi"""
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)

    # Synchronous tarzda update ni ishlatish
    try:
        asyncio.run(application.process_update(update))
    except Exception as e:
        print("Webhook processing error:", e)
    return "ok"

# Oddiy health check route
@app.route("/")
def index():
    return "Bot is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
