import asyncio
import threading
from flask import Flask, request
from telegram import Update
from telegram.ext import Application
from config import BOT_TOKEN, ADMIN_ID, WEBHOOK_URL, CHECK_INTERVAL
from scheduler import check_orders, ensure_orders
from notifier import init_notifier

app = Flask(__name__)

# 🔹 Yangi event loop (Python 3.13 friendly)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# 🔹 Telegram bot (async context uchun)
tg_app = Application.builder().token(BOT_TOKEN).build()

# 🔹 Notifier init
init_notifier(tg_app, loop, ADMIN_ID)

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.json, tg_app.bot)
    loop.create_task(tg_app.update_queue.put(update))
    return "ok"

def background_loop():
    ensure_orders()
    while True:
        check_orders()
        loop.run_until_complete(asyncio.sleep(CHECK_INTERVAL))

def start_bg():
    threading.Thread(target=background_loop, daemon=True).start()

if __name__ == "__main__":
    async def main():
        # 🔹 Telegram initialize
        await tg_app.initialize()
        await tg_app.bot.set_webhook(WEBHOOK_URL)

        # 🔹 Background start
        start_bg()

        # 🔹 Flask server (sync)
        app.run(host="0.0.0.0", port=10000)

    loop.run_until_complete(main())
