import asyncio
from telegram.ext import Application
from config import BOT_TOKEN, ADMIN_ID, CHECK_INTERVAL
from scheduler import check_orders, ensure_orders
from notifier import init_notifier
import threading

# 🔹 Yangi event loop yaratish
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# 🔹 Telegram botni yaratish (polling uchun)
tg_app = Application.builder().token(BOT_TOKEN).build()

# 🔹 Notifierni init qilish
init_notifier(tg_app, loop, ADMIN_ID)

# 🔹 Background zakazlar uchun thread
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

        # 🔹 Background ishga tushirish
        start_bg()

        # 🔹 Pollingni ishga tushurish
        await tg_app.run_polling()

    # 🔹 Loopni ishga tushirish
    loop.run_until_complete(main())
