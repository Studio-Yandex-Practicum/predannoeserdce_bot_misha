import re

from telegram import Update
from telegram.ext import ContextTypes

from constants import RegexText


async def fullname_validate(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> bool:
    """
    Проверка введенных данных на соответсвие:

    1. Введено 2 или более слов;
    2. Слова набраны кириллицей;
    3. Слова начинаются с прописной буквы, остальные строчные;
    4. Несоответствующий текст отсутствует.
    """
    words = update.message.text.split()
    match = re.findall(RegexText.USER_FULLNAME, update.message.text)
    return set(words) == set(match) and len(match) >= 2


async def email_validate(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> bool:
    """Проверка введенных данных на соответсвие email."""
    return bool(re.compile(pattern=RegexText.EMAIL).match(update.message.text))


async def phone_validate(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> bool:
    """Проверка введенных данных на соответсвие номеру телефона."""
    return bool(re.compile(pattern=RegexText.PHONE).match(update.message.text))
