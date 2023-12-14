import asyncio

from telegram import Update
from telegram.ext import ContextTypes

import keyboards as kb
from constants import LINK_ITEMS, MENU_ITEMS, MENU_SLEEP, START_SLEEP
from message_config import MESSAGES
from requests_db import get_faq
from settings import bot_logger


def update_faq_list() -> None:
    """Обновляет список частых вопросов."""
    global faq_list
    faq_list = get_faq()
    bot_logger.info(msg="Список частых вопросов обновлён")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отвечает пользователю на команду /start."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=MESSAGES["start"]
    )
    await show_menu_btn(update=update, context=context, delay=START_SLEEP)


async def show_menu_btn(
    update: Update, context: ContextTypes.DEFAULT_TYPE, delay: int | None
) -> None:
    """Показывает кнопку вызова основного меню."""
    if delay:
        await asyncio.sleep(delay=delay)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=MESSAGES["menu_btn"],
        reply_markup=await kb.get_menu_button(),
    )
    bot_logger.info(msg="Показана кнопка вызова главного меню")


async def show_main_menu(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Показывает основное меню."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=MESSAGES["menu"],
        reply_markup=await kb.get_main_menu(),
    )
    bot_logger.info(msg="Показано главное меню")


async def alert_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Отвечает пользователю на попытку отправить неподдерживаемый контент."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=MESSAGES["alert_message"]
    )


async def handle_menu_buttons(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Обрабатывает нажатие кнопок меню."""
    if update.message.text in list(MENU_ITEMS.keys()):
        await globals()[MENU_ITEMS[update.message.text]](update, context)
    elif update.message.text in list(LINK_ITEMS.keys()):
        await url_button_click(update=update, context=context)
    elif update.message.text == "МЕНЮ":
        await show_main_menu(update=update, context=context)
    else:
        await alert_message(update=update, context=context)
        bot_logger.info(
            msg=f"Прислано необрабатываемое сообщение: {update.message.text}"
        )


async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает нажатие кнопки `Частые вопросы`."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Что вы хотите узнать?",
        reply_markup=await kb.remove_menu(),
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Выберите вопрос, который вас интересует:",
        reply_markup=await kb.get_faq_menu(faq_questions=faq_list),
    )
    bot_logger.info(msg="Обработка кнопки `Частые вопросы`")


async def url_button_click(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Обрабатывает нажатие кнопки с переходом на сайт."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Нажмите на кнопку, чтобы перейди на сайт.",
        reply_markup=await kb.get_url_button(
            btn_attrs=LINK_ITEMS[update.message.text],
        ),
    )
    bot_logger.info(msg=f"Обработка кнопки `{update.message.text}`")
    await show_menu_btn(update=update, context=context, delay=MENU_SLEEP)


async def subscribe(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Здесь должна быть обработка "
        "подписки на рассылку, но её пока нет",
    )
    await show_menu_btn(update=update, context=context, delay=1),
