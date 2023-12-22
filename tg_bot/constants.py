import logging
import os
from enum import Enum

from dotenv import load_dotenv

from utils import LinkButtonAttributes

load_dotenv()

# Константы для телеграма
TELEGRAM_TOKEN = os.getenv(key="TELEGRAM_TOKEN")
ADMIN_CHAT_ID = os.getenv(key="ADMIN_CHAT_ID")
ADMIN_LOGIN = os.getenv('ADMIN_LOGIN')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

# Кнопки меню
MENU_ITEMS: dict[str, str] = {
    "частые вопросы": "faq",
    "подписаться на рассылку": "subscribe",
}
LINK_ITEMS: dict[str, LinkButtonAttributes] = {
    "попечительство": LinkButtonAttributes(
        text="Условия попечительства можно посмотреть на сайте",
        url="https://predannoeserdce.ru/programmy-prijuta/popechitelstvo/",
    ),
    "пожертвование": LinkButtonAttributes(
        text="Сделать пожертвование можно перейдя по ссылке",
        url="https://predannoeserdce.ru/help/",
    ),
    "взять котика": LinkButtonAttributes(
        text="Взять котика домой можно по ссылке",
        url="https://predannoeserdce.ru/howtohelp/take-home/",
    ),
    "посмотреть котиков": LinkButtonAttributes(
        text="Посмотреть котиков можно по ссылке",
        url="https://predannoeserdce.ru/catalog-opeka/",
    ),
    "перейти на сайт приюта": LinkButtonAttributes(
        text="Перейти на главную страницу",
        url="https://predannoeserdce.ru/",
    ),
}
MENU_LAYOUT = 3
FAQ_PER_PAGE = 5


# Отдельные кнопки
class OneButtonItems:
    MENU = "меню"
    CANCEL = "отмена"


# Задержки
START_SLEEP = 1
MENU_SLEEP = 3


# Получение и обновление списка вопросов
SERVER_API_FAQ_URL = os.getenv(key="SERVER_API_FAQ_URL")
FAQ_UPDATE_INTERVAL_MINUTES = 10


# Проверки введенного текста
class RegexText:
    USER_FULLNAME = r"(\b[А-Я]{1}[а-я]+\b)"
    CANCEL = r"^отмена$"
    EMAIL = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    PHONE = r"^\+7\d{10}$"


# Стадии разговора
class ConvState(int, Enum):
    EMAIL = 0
    PHONE = 1
    SUBJECT = 2
    QUESTION = 3
    SEND = 4
    SUBSCRIBE = 5


class PaginationCallback:
    FIRST_PAGE = "first_page"
    PREV_PAGE = "prev_page"
    NEXT_PAGE = "next_page"
    LAST_PAGE = "last_page"


class MainCallbacks:
    CUSTOM_QUESTION = "custom_question"
    TG_QUESTION = "tg_question"
    EMAIL_QUESTION = "email_question"


# Настройки логгера:
class LogSetting:
    FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LEVEL = logging.INFO
    NAME = "tg_bot"
    FILENAME = "bot_logs/tg_bot.log"
    ENCODING = "utf8"
    FILESIZE = 1024 * 1024
    FILECOUNT = 3


# Токен
SERVER_API_TOKEN_URL = os.getenv('SERVER_API_TOKEN_URL')
TOKEN_UPDATE = 12 # в часах

#Подписка
SERVER_API_CUSTOMER_URL = os.getenv('SERVER_API_CUSTOMER_URL')