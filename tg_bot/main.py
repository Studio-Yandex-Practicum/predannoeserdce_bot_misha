from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
)

from constants import MINUTES_FAQ_UPDATE_INTERVAL, TELEGRAM_TOKEN
from handlers import (
    alert_message,
    handle_menu_buttons,
    show_menu_btn,
    start,
    update_faq_list,
)

scheduller = AsyncIOScheduler()
scheduller.add_job(
    func=update_faq_list,
    trigger="interval",
    minutes=MINUTES_FAQ_UPDATE_INTERVAL,
)
scheduller.start()
update_faq_list()


if __name__ == "__main__":
    application = ApplicationBuilder().token(token=TELEGRAM_TOKEN).build()
    handlers = [
        CommandHandler(command="start", callback=start),
        CommandHandler(command="menu", callback=show_menu_btn),
        MessageHandler(
            filters=(filters.AUDIO | filters.PHOTO), callback=alert_message
        ),
        MessageHandler(filters=(filters.TEXT), callback=handle_menu_buttons),
    ]
    for handler in handlers:
        application.add_handler(handler=handler)
    application.run_polling()
