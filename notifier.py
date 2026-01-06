from telegram.ext import Application

tg_app: Application | None = None
ADMIN_ID: int | None = None

def init_notifier(application: Application, admin_id: int):
    global tg_app, ADMIN_ID
    tg_app = application
    ADMIN_ID = admin_id

async def send_admin(text: str):
    if not tg_app or not ADMIN_ID:
        return
    await tg_app.bot.send_message(
        chat_id=ADMIN_ID,
        text=text
    )
