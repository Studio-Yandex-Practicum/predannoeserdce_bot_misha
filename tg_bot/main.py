import re

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Update
from telegram.ext import (ApplicationBuilder, CallbackQueryHandler,
                          CommandHandler, ContextTypes, ConversationHandler,
                          MessageHandler, filters)

import keyboards as kb
from constants import (FAQ_UPDATE_INTERVAL_MINUTES, START_SLEEP,
                       TELEGRAM_TOKEN, TOKEN_UPDATE, ConvState, MainCallbacks,
                       OneButtonItems, RegexText)
from handlers import (conv_cancel, conv_end, conv_get_email, conv_get_phone,
                      conv_get_question, conv_get_subject,
                      handle_alert_message, handle_conv_callback,
                      handle_conv_message, handle_faq_callback,
                      handle_menu_buttons, handle_show_main_menu, update_faq)
from message_config import MESSAGES, SubTextButton
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
    hours=TOKEN_UPDATE,
)
scheduller.start()
update_faq()
get_token()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отвечает пользователю на команду /start."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=MESSAGES["start"],
        reply_markup=await kb.remove_menu(),
    )
    await handle_show_main_menu(
        update=update, context=context, delay=START_SLEEP
    )


def main() -> None:
    """Запуск бота."""
    application = ApplicationBuilder().token(token=TELEGRAM_TOKEN).build()
    cancel_pattern = re.compile(
        pattern=RegexText.CANCEL,
        flags=re.IGNORECASE
        )
    skip_cancel_pattern = re.compile(
        rf"^(?!.*\b{OneButtonItems.CANCEL.upper()}\b).*$"
        )
    handlers = [
        ConversationHandler(
            entry_points=[
                CallbackQueryHandler(
                    callback=handle_conv_callback,
                    pattern=MainCallbacks.TG_QUESTION,
                ),
                CallbackQueryHandler(
                    callback=handle_conv_callback,
                    pattern=MainCallbacks.EMAIL_QUESTION,
                ),
                MessageHandler(
                    filters.Text(
                        f"{SubTextButton.START} | {SubTextButton.RETURN}"
                        ),
                    handle_conv_message,
                )
            ],
            states={
                ConvState.EMAIL: [
                    MessageHandler(
                        filters=(filters.Regex(pattern=skip_cancel_pattern)),
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
                    filters=(filters.Regex(pattern=cancel_pattern)),
                    callback=conv_cancel,
                ),
                CommandHandler(command="menu", callback=conv_cancel),
            ],
        ),
        CommandHandler(command="start", callback=start),
        CommandHandler(command="menu", callback=handle_show_main_menu),
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
    ]
    for handler in handlers:
        application.add_handler(handler=handler)
    application.run_polling()


if __name__ == "__main__":
    main()
