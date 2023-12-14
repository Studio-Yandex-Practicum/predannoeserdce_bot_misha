from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from constants import MINUTES_FAQ_UPDATE_INTERVAL, START_SLEEP, TELEGRAM_TOKEN
from handlers import (
    handle_alert_message,
    handle_menu_buttons,
    handle_show_main_menu,
    update_faq,
)
from message_config import MESSAGES

scheduller = AsyncIOScheduler()
scheduller.add_job(
    func=update_faq,
    trigger="interval",
    minutes=MINUTES_FAQ_UPDATE_INTERVAL,
)
scheduller.start()
update_faq()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отвечает пользователю на команду /start."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=MESSAGES["start"]
    )
    await handle_show_main_menu(
        update=update, context=context, delay=START_SLEEP
    )


if __name__ == "__main__":
    application = ApplicationBuilder().token(token=TELEGRAM_TOKEN).build()
    handlers = [
        CommandHandler(command="start", callback=start),
        CommandHandler(command="menu", callback=handle_show_main_menu),
        MessageHandler(
            filters=(filters.AUDIO | filters.PHOTO),
            callback=handle_alert_message,
        ),
        MessageHandler(filters=(filters.TEXT), callback=handle_menu_buttons),
    ]
    for handler in handlers:
        application.add_handler(handler=handler)
    application.run_polling()
