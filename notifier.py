import asyncio

tg_app = None
ADMIN_ID = None

def init_notifier(application, admin_id):
    global tg_app, ADMIN_ID
    tg_app = application
    ADMIN_ID = admin_id

def send_admin(text):
    if not tg_app or not ADMIN_ID:
        return
    asyncio.create_task(tg_app.bot.send_message(chat_id=ADMIN_ID, text=text))
