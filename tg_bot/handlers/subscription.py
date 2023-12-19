import os
from http import HTTPStatus
from typing import Dict

import requests
from telegram import Update
from telegram.ext import (CallbackQueryHandler, ContextTypes,
                          ConversationHandler, MessageHandler, filters)

import keyboards as kb
from constants import API_CUSTOMER, SubState
from message_config import CUSTOMER, SubMessageText
from utils import format_error_messages


def facts_to_str(user_data: Dict[str, str]) -> str:
    facts = [f"{CUSTOMER[key]} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        SubMessageText.START,
        reply_markup=await kb.get_customer_menu(),
    )
    return SubState.CHOOSING


async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.callback_query.data
    context.user_data[SubMessageText.CHOICE] = text
    await update.callback_query.message.edit_text(f"{SubMessageText.WRITE} {CUSTOMER[text]}")

    return SubState.TYPING_REPLY


async def received_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = context.user_data
    text = update.message.text
    category = user_data[SubMessageText.CHOICE]
    user_data[category] = text
    if all(key in user_data for key in CUSTOMER.keys()):
        # Показываем кнопку "Подписаться"
        markup =await  kb.get_sub_menu()
    else:
        markup =await  kb.get_customer_menu()
    del user_data[SubMessageText.CHOICE]
    await update.message.reply_text(
        f"{SubMessageText.USER_DATE}"
        f"{facts_to_str(user_data)}",
        reply_markup=markup,
    )

    return SubState.CHOOSING


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = context.user_data
    api_url = API_CUSTOMER
    token = os.getenv('ADMIN_TOKEN')
    if SubMessageText.CHOICE in user_data:
        del user_data[SubMessageText.CHOICE]

    data_to_send = {
        'email': user_data['email'],
        'name': user_data['name'],
        'phone': user_data['phone'],
        'tg_id': str(update.callback_query.from_user.id)
    }

    data_to_user = {
        'Email': user_data['email'],
        'Имя': user_data['name'],
        'Телефон': user_data['phone'],
    }

    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }

    response = requests.post(api_url, json=data_to_send, headers=headers)
    if response.status_code == HTTPStatus.CREATED:
        text = f"{SubMessageText.DONE}{facts_to_str(data_to_user)}"
    else:
        error = format_error_messages(response.text)
        text = f"{SubMessageText.ERROR}{error}"
    await update.callback_query.message.edit_text(
        text
    )
    user_data.clear()
    return ConversationHandler.END


sub_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Text(['Подписаться на рассылку']), start)],
    states={
        SubState.CHOOSING: [
            CallbackQueryHandler(regular_choice, pattern=f"^({'|'.join(CUSTOMER.keys())})$"),
        ],
        SubState.TYPING_CHOICE: [
            MessageHandler(
                filters.TEXT , regular_choice
            )
        ],
        SubState.TYPING_REPLY: [
            MessageHandler(filters.TEXT, received_information,)
        ],
    },
    fallbacks=[CallbackQueryHandler(done, pattern="^sub$")],
)
