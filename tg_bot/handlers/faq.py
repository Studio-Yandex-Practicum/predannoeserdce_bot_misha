from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

import core.keyboards as kb
from core.constants import MainCallbacks, PaginationCallback
from core.message_config import ConversationTextMessage, MainMessage
from core.requests_db import get_faq
from core.services import get_pages_count


def update_faq() -> None:
    """Обновляет список частых вопросов."""
    global faq_dict
    faq_dict = get_faq()


async def handle_faq_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Обрабатывает нажатие кнопки `Частые вопросы`."""
    context.user_data["category"] = None
    query = update.callback_query
    callback = query.data if query else None
    categories = list(faq_dict.keys())
    if callback in categories:
        await handle_category_button(update=update, context=context)
        return None
    cur_page = context.user_data.get("categories_page", None)
    if not cur_page or not callback:
        cur_page = 1
        context.user_data["categories_page"] = cur_page
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=MainMessage.CATEGORY,
            reply_markup=await kb.get_categories_menu(
                categories=categories, page=cur_page
            ),
        )
        return None
    new_page = await get_page_number(
        callback=callback,
        queryset=categories,
        page=cur_page,
    )
    await update.effective_message.edit_text(
        text=MainMessage.CATEGORY,
        reply_markup=await kb.get_categories_menu(
            categories=categories, page=new_page
        ),
    )
    context.user_data["categories_page"] = new_page
    await query.answer()


async def handle_category_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Обрабатывает нажатие кнопки с категорией частых вопросов."""
    category = context.user_data.get("category", None)
    if not category:
        context.user_data["questions_page"] = None
    query = update.callback_query
    callback = query.data if query else None
    if (
        callback != MainCallbacks.BACK_TO_FAQ
        and callback not in vars(PaginationCallback).values()
    ):
        category = callback
        context.user_data["category"] = category
    questions = [{key: value} for key, value in faq_dict[category].items()]
    cur_page = context.user_data.get("questions_page", None)
    if not cur_page:
        cur_page = 1
    new_page = await get_page_number(
        callback=callback,
        queryset=questions,
        page=cur_page,
    )
    await update.effective_message.edit_text(
        text=MainMessage.FAQ,
        reply_markup=await kb.get_faq_menu(
            faq_questions=questions, page=new_page
        ),
    )
    context.user_data["questions_page"] = new_page
    await query.answer()


async def get_page_number(callback, queryset, page: int) -> int:
    pages_count = await get_pages_count(queryset=queryset)
    if callback == PaginationCallback.FIRST_PAGE:
        page = 1
    elif callback == PaginationCallback.LAST_PAGE:
        page = pages_count
    elif callback == PaginationCallback.NEXT_PAGE:
        page += 1
    elif callback == PaginationCallback.PREV_PAGE:
        page -= 1
    return page


async def handle_faq_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Обрабатывает частые вопросы. Выдаёт ответы."""
    query = update.callback_query
    callback = query.data
    if callback.isdigit():
        category = context.user_data.get("category", None)
        if not category:
            await query.answer()
            return None
        data = faq_dict[category][callback]
        text = ConversationTextMessage.ANSWER_BY_FAQ % (
            tuple(data.values())[:2]
        )
        await query.edit_message_text(
            text=text,
            reply_markup=await kb.get_back_to_faq(),
            parse_mode=ParseMode.HTML,
        )
        await query.answer()
    elif context.user_data.get("category", None) is not None:
        await handle_category_button(update, context)
    else:
        await handle_faq_button(update, context)
