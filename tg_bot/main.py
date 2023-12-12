from constants import TELEGRAM_TOKEN
from handlers import alert_message, handle_menu_buttons, show_menu_btn, start
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
)

if __name__ == "__main__":
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    handlers = [
        CommandHandler("start", start),
        CommandHandler("menu", show_menu_btn),
        MessageHandler((filters.AUDIO | filters.PHOTO), alert_message),
        MessageHandler((filters.TEXT), handle_menu_buttons),
    ]
    for handler in handlers:
        application.add_handler(handler)
    application.run_polling()
