import asyncio

import keyboards as kb
from constants import MENU_ITEMS, MENU_SLEEP, START_SLEEP
from message_config import MESSAGES
from settings import logger
from telegram import Update
from telegram.ext import ContextTypes


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
        reply_markup=await kb.show_menu_button(),
    )


async def show_main_menu(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Показывает основное меню."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=MESSAGES["menu"],
        reply_markup=await kb.show_main_menu(),
    )


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
    """Обрабатывает нажатие кнопок."""
    if update.message.text in list(MENU_ITEMS.keys()):
        await globals()[MENU_ITEMS[update.message.text]](update, context)
    elif update.message.text == "МЕНЮ":
        await show_main_menu(update=update, context=context)
    else:
        await alert_message(update=update, context=context)


async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(msg="Обработка кнопки `Частые вопросы`")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Обработка кнопки `Частые вопросы`",
        reply_markup=await kb.remove_menu(),
    )
    await show_menu_btn(update=update, context=context, delay=MENU_SLEEP)


async def email_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    logger.info(msg="Обработка кнопки `Задать по email`")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Обработка кнопки `Задать по email`",
        reply_markup=await kb.remove_menu(),
    )
    await show_menu_btn(update=update, context=context, delay=MENU_SLEEP)


async def custom_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    logger.info(msg="Обработка кнопки `Задать вопрос`")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Обработка кнопки `Задать вопрос`",
        reply_markup=await kb.remove_menu(),
    )
    await show_menu_btn(update=update, context=context, delay=MENU_SLEEP)


async def see_cats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(msg="Обработка кнопки `Посмотреть котиков`")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Обработка кнопки `Посмотреть котиков`",
        reply_markup=await kb.remove_menu(),
    )
    await show_menu_btn(update=update, context=context, delay=MENU_SLEEP)


async def adopt_cat(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    logger.info(msg="Обработка кнопки `Взять котика`")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Обработка кнопки `Взять котика`",
        reply_markup=await kb.remove_menu(),
    )
    await show_menu_btn(update=update, context=context, delay=MENU_SLEEP)


async def patronage(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    logger.info(msg="Обработка кнопки `Попечительство`")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Обработка кнопки `Попечительство``",
        reply_markup=await kb.remove_menu(),
    )
    await show_menu_btn(update=update, context=context, delay=MENU_SLEEP)


async def donat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(msg="Обработка кнопки `Пожертвования`")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Обработка кнопки `Пожертвования`",
        reply_markup=await kb.remove_menu(),
    )
    await show_menu_btn(update=update, context=context, delay=MENU_SLEEP)
