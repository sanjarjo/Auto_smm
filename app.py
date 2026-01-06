from telegram.ext import Application, CommandHandler
from config import BOT_TOKEN

def start(update, context):
    update.message.reply_text("Bot ishlayapti ✅")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.run_polling()

if __name__ == "__main__":
    main()
