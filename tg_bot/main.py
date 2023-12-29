import re

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

import core.keyboards as kb
from core.apscher import scheduller_initial
from core.constants import (
    LINK_BUTTONS,
    MASCOT_FILENAME,
    START_SLEEP,
    TELEGRAM_TOKEN,
    MainCallbacks,
    MenuFuncButton,
)
from handlers.ban import handle_to_ban
from handlers.basic import (
    handle_alert_message,
    handle_error_callback,
    handle_show_main_menu,
    handle_text_message,
    handle_url_button,
    handle_custom_question_button,
)
from handlers.conv_data_collection import (
    data_collect_handler,
    tg_question_handler,
)
from handlers.faq import (
    handle_category_button,
    handle_faq_button,
    handle_faq_callback,
    update_faq,
)
from handlers.subscribe import unsubscribe
from core.message_config import MainMessage
from core.requests_db import get_token


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отвечает пользователю на команду /start."""
    with open(file=MASCOT_FILENAME, mode="rb") as photo:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo,
            caption=MainMessage.START,
            reply_markup=await kb.remove_menu(),
        )
    await handle_show_main_menu(
        update=update, context=context, delay=START_SLEEP
    )


def main() -> None:
    """Запуск бота."""
    application = ApplicationBuilder().token(token=TELEGRAM_TOKEN).build()
    bot = application.bot

    scheduller = scheduller_initial(bot=bot)
    scheduller.start()
    update_faq()
    get_token()

    handlers = [
        data_collect_handler,
        tg_question_handler,
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
                        pattern=rf"{MenuFuncButton.CUSTOM_QUESTION.value}",
                        flags=re.IGNORECASE,
                    )
                )
            ),
            callback=handle_custom_question_button,
        ),
        MessageHandler(
            filters=(
                filters.Regex(
                    pattern=re.compile(
                        pattern=rf"{MenuFuncButton.UNSUBSCRIBE.value}",
                        flags=re.IGNORECASE,
                    )
                )
            ),
            callback=unsubscribe,
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
        CallbackQueryHandler(
            callback=handle_to_ban, pattern=MainCallbacks.USER_TO_BAN
        ),
        CallbackQueryHandler(
            callback=handle_faq_button,
            pattern=MainCallbacks.BACK_TO_CATEGORIES,
        ),
        CallbackQueryHandler(
            callback=handle_category_button,
            pattern=MainCallbacks.BACK_TO_FAQ,
        ),
        CallbackQueryHandler(callback=handle_faq_callback),
        MessageHandler(
            filters=(~filters.TEXT),
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
