# notifier.py
import asyncio

tg_app = None
loop = None
ADMIN_ID = None

def init_notifier(application, event_loop, admin_id):
    global tg_app, loop, ADMIN_ID
    tg_app = application
    loop = event_loop
    ADMIN_ID = admin_id

def send_admin(text):
    if not tg_app or not loop or not ADMIN_ID:
        return

    asyncio.run_coroutine_threadsafe(
        tg_app.bot.send_message(chat_id=ADMIN_ID, text=text),
        loop
    )
