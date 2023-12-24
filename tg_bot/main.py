import re

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

import keyboards as kb
from constants import (
    FAQ_UPDATE_INTERVAL_MINUTES,
    LINK_BUTTONS,
    START_SLEEP,
    TELEGRAM_TOKEN,
    TOKEN_UPDATE_HOURS,
    ConvState,
    MainCallbacks,
    MenuFuncButton,
    OneButtonItems,
)
from handlers import (
    conv_cancel,
    conv_end,
    conv_get_email,
    conv_get_phone,
    conv_get_question,
    conv_get_subject,
    conv_start,
    handle_alert_message,
    handle_error_callback,
    handle_faq_button,
    handle_faq_callback,
    handle_show_main_menu,
    handle_text_message,
    handle_url_button,
    update_faq,
)
from message_config import MainMessage
from requests_db import get_token

scheduller = AsyncIOScheduler()
scheduller.add_job(
    func=update_faq,
    trigger="interval",
    minutes=FAQ_UPDATE_INTERVAL_MINUTES,
)
scheduller.add_job(
    func=get_token,
    trigger="interval",
    hours=TOKEN_UPDATE_HOURS,
)
scheduller.start()
update_faq()
get_token()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отвечает пользователю на команду /start."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=MainMessage.START,
        reply_markup=await kb.remove_menu(),
    )
    await handle_show_main_menu(
        update=update, context=context, delay=START_SLEEP
    )


def main() -> None:
    """Запуск бота."""
    application = ApplicationBuilder().token(token=TELEGRAM_TOKEN).build()
    cancel_pattern = re.compile(
        pattern=rf"^{OneButtonItems.CANCEL}$", flags=re.IGNORECASE
    )
    skip_cancel_pattern = re.compile(
        pattern=rf"^(?!.*\b{OneButtonItems.CANCEL}\b).*$", flags=re.IGNORECASE
    )
    subscribe_pattern = re.compile(
        pattern=rf"^(?:{MenuFuncButton.SUBSCRIBE.value}|"
        f"{OneButtonItems.RETURN})$",
        flags=re.IGNORECASE,
    )
    handlers = [
        ConversationHandler(
            entry_points=[
                CallbackQueryHandler(
                    callback=conv_start,
                    pattern=MainCallbacks.TG_QUESTION,
                ),
                CallbackQueryHandler(
                    callback=conv_start,
                    pattern=MainCallbacks.EMAIL_QUESTION,
                ),
                MessageHandler(
                    filters=filters.Regex(pattern=subscribe_pattern),
                    callback=conv_start,
                ),
            ],
            states={
                ConvState.EMAIL: [
                    MessageHandler(
                        filters=(
                            filters.Regex(pattern=skip_cancel_pattern)
                            & ~filters.COMMAND
                        ),
                        callback=conv_get_email,
                    ),
                ],
                ConvState.PHONE: [
                    MessageHandler(
                        filters=(filters.Regex(pattern=skip_cancel_pattern)),
                        callback=conv_get_phone,
                    ),
                ],
                ConvState.SUBJECT: [
                    MessageHandler(
                        filters=(filters.Regex(pattern=skip_cancel_pattern)),
                        callback=conv_get_subject,
                    )
                ],
                ConvState.QUESTION: [
                    MessageHandler(
                        filters=(filters.Regex(pattern=skip_cancel_pattern)),
                        callback=conv_get_question,
                    )
                ],
                ConvState.SEND: [
                    MessageHandler(
                        filters=(filters.Regex(pattern=skip_cancel_pattern)),
                        callback=conv_end,
                    )
                ],
            },
            fallbacks=[
                MessageHandler(
                    filters=(
                        filters.Regex(pattern=cancel_pattern) | filters.COMMAND
                    ),
                    callback=conv_cancel,
                ),
            ],
        ),
        MessageHandler(
            filters=(
                filters.Regex(
                    pattern=re.compile(
                        pattern=rf"{MenuFuncButton.FAQ.value}",
                        flags=re.IGNORECASE,
                    )
                )
            ),
            callback=handle_faq_button,
        ),
        MessageHandler(
            filters=(
                filters.Regex(
                    pattern=re.compile(
                        pattern=rf"{'|'.join(LINK_BUTTONS.keys())}",
                        flags=re.IGNORECASE,
                    )
                )
            ),
            callback=handle_url_button,
        ),
        MessageHandler(
            filters=(filters.TEXT & ~filters.COMMAND),
            callback=handle_text_message,
        ),
        CallbackQueryHandler(
            callback=handle_error_callback, pattern=MainCallbacks.SERVER_ERROR
        ),
        CallbackQueryHandler(callback=handle_faq_callback),
        MessageHandler(
            filters=(filters.AUDIO | filters.PHOTO | filters.Sticker.ALL),
            callback=handle_alert_message,
        ),
        CommandHandler(command="start", callback=start),
        CommandHandler(command="menu", callback=handle_show_main_menu),
    ]
    for handler in handlers:
        application.add_handler(handler=handler)
    application.run_polling()


if __name__ == "__main__":
    main()
