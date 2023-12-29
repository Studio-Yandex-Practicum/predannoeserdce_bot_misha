import re

from telegram import Update
from telegram.ext import ContextTypes

from core.constants import RegexText


async def fullname_validate(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> bool:
    """
    Проверка введенных данных на соответсвие:

    1. Введено 2 или более слов;
    2. Слова набраны кириллицей;
    3. Несоответствующий текст отсутствует.
    """
    text = update.message.text.title()
    words = text.split()
    match = re.findall(pattern=RegexText.USER_FULLNAME, string=text)
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
