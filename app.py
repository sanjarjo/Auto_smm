import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Tokenni config.py dan import qilamiz
from config import BOT_TOKEN

app = Flask(__name__)

# Telegram /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Bot ishga tushdi.")

# Telegram botni ishga tushiramiz
application = ApplicationBuilder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))

# Webhook route
@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
def webhook():
    """Telegram POST requestlarini qabul qiladi"""
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

# Oddiy route (health check yoki index)
@app.route("/")
def index():
    return "Bot is running!"

if __name__ == "__main__":
    # Flask serverni ishga tushiramiz
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
