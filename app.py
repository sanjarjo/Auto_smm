import asyncio
import threading
from telegram.ext import Application
from config import BOT_TOKEN, ADMIN_ID, CHECK_INTERVAL
from scheduler import check_orders, ensure_orders
from notifier import init_notifier

# 🔹 Yangi event loop yaratish (Python 3.13 friendly)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# 🔹 Telegram bot (async Application)
tg_app = Application.builder().token(BOT_TOKEN).build()

# 🔹 Notifierni init qilish
init_notifier(tg_app, loop, ADMIN_ID)

# 🔹 Background task: zakazlarni tekshirish
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

        # 🔹 Pollingni boshlash
        await tg_app.start()
        await tg_app.updater.start_polling()

        # 🔹 Background threadni ishga tushirish
        start_bg()

        # 🔹 Botni loopda ushlab turish
        await tg_app.updater.wait_closed()

    # 🔹 Async loopni ishga tushurish
    loop.run_until_complete(main())
