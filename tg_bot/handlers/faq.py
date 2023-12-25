from telegram import Message, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

import keyboards as kb
from constants import MainCallbacks, PaginationCallback
from message_config import ConversationTextMessage, MainMessage
from requests_db import get_faq
from services import faq_pages_count


def update_faq() -> None:
    """Обновляет список частых вопросов."""
    global faq_dict
    faq_dict = get_faq()


async def handle_faq_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> Message | None:
    """Обрабатывает нажатие кнопки `Частые вопросы`."""
    query = update.callback_query
    order = query.data if query else None
    pages_count = await faq_pages_count(faq_dict=faq_dict)
    page = context.user_data.get("page", None)
    if not page or not order:
        page = 1
        context.user_data["page"] = page
        return await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=MainMessage.FAQ,
            reply_markup=await kb.get_faq_menu(
                faq_questions=faq_dict, page=page
            ),
        )
    elif order == PaginationCallback.FIRST_PAGE:
        page = 1
    elif order == PaginationCallback.LAST_PAGE:
        page = pages_count
    elif order == PaginationCallback.NEXT_PAGE:
        page += 1
    elif order == PaginationCallback.PREV_PAGE:
        page -= 1
    await update.effective_message.edit_text(
        text=MainMessage.FAQ,
        reply_markup=await kb.get_faq_menu(faq_questions=faq_dict, page=page),
    )
    context.user_data["page"] = page
    await query.answer()


async def handle_faq_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Обрабатывает частые вопросы. Выдаёт ответы."""
    query = update.callback_query
    order = query.data
    if order.isdigit():
        data = faq_dict[order]
        text = ConversationTextMessage.ANSWER_BY_FAQ % (
            tuple(data.values())[:2]
        )
        await query.edit_message_text(
            text=text,
            reply_markup=await kb.get_back_to_faq(),
            parse_mode=ParseMode.HTML,
        )
    elif order != MainCallbacks.CUSTOM_QUESTION:
        return await handle_faq_button(update=update, context=context)
    else:
        await query.edit_message_text(
            text=ConversationTextMessage.COMMUNICATION_WAY,
            reply_markup=await kb.get_communication_way(),
        )
    await query.answer()
