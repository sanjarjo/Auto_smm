import asyncio, threading
from flask import Flask, request
from telegram import Update
from telegram.ext import Application
from config import BOT_TOKEN, ADMIN_ID, WEBHOOK_URL, CHECK_INTERVAL
from scheduler import check_orders, ensure_orders
from notifier import init_notifier

app = Flask(__name__)
tg_app = Application.builder().token(BOT_TOKEN).build()
loop = asyncio.get_event_loop()

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.json, tg_app.bot)
    loop.create_task(tg_app.process_update(update))
    return "ok"

def background_loop():
    ensure_orders()
    while True:
        check_orders()
        asyncio.run(asyncio.sleep(CHECK_INTERVAL))

def start_bg():
    threading.Thread(target=background_loop, daemon=True).start()

if __name__ == "__main__":
    loop.create_task(tg_app.initialize())
    loop.create_task(tg_app.bot.set_webhook(WEBHOOK_URL))

    # 🔥 MUHIM QATOR
    init_notifier(tg_app, loop, ADMIN_ID)

    start_bg()
    app.run(host="0.0.0.0", port=10000)
