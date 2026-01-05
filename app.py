import asyncio
import threading
from flask import Flask, request
from telegram import Update
from telegram.ext import Application
from config import BOT_TOKEN, ADMIN_ID, WEBHOOK_URL, CHECK_INTERVAL
from scheduler import check_orders, ensure_orders
from notifier import init_notifier

app = Flask(__name__)

# 🔹 Async loop yaratish to‘g‘ri
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# 🔹 Telegram bot
tg_app = Application.builder().token(BOT_TOKEN).build()

# 🔹 Notifier init
init_notifier(tg_app, loop, ADMIN_ID)

@app.route("/webhook", methods=["POST"])
def webhook():
    """Telegram webhook POST qabul qiladi"""
    update = Update.de_json(request.json, tg_app.bot)
    loop.create_task(tg_app.update_queue.put(update))
    return "ok"

def background_loop():
    """Background zakaz monitoring"""
    ensure_orders()
    while True:
        check_orders()
        loop.run_until_complete(asyncio.sleep(CHECK_INTERVAL))

def start_bg():
    threading.Thread(target=background_loop, daemon=True).start()

if __name__ == "__main__":
    # 🔹 Async initialize va webhook
    loop.run_until_complete(tg_app.initialize())
    loop.run_until_complete(tg_app.bot.set_webhook(WEBHOOK_URL))

    # 🔹 Background start
    start_bg()

    # 🔹 Flask server
    app.run(host="0.0.0.0", port=10000)
