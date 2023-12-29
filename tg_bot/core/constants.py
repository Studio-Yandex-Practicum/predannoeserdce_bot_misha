import logging
import os
from enum import Enum

from dotenv import load_dotenv

from core.utils import LinkButtonAttributes

load_dotenv()

# Константы для телеграма
TELEGRAM_TOKEN = os.getenv(key="TELEGRAM_TOKEN")
ADMIN_CHAT_ID = os.getenv(key="ADMIN_CHAT_ID")
ADMIN_LOGIN = os.getenv("ADMIN_LOGIN")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


# Функциональные кнопки меню
class MenuFuncButton(str, Enum):
    FAQ = "частые вопросы"
    CUSTOM_QUESTION = "задать вопрос"
    SUBSCRIBE = "подписаться на рассылку"
    UNSUBSCRIBE = "отписаться от рассылки"


# Ссылочные кнопки меню
LINK_BUTTONS: dict[str, LinkButtonAttributes] = {
    "сделать пожертвование": LinkButtonAttributes(
        text="Сделать пожертвование можно перейдя по ссылке",
        url="https://predannoeserdce.ru/sms-pozhertvovanie/",
    ),
    "список животных": LinkButtonAttributes(
        text="Перейти на страницу со списком животных в приюте",
        url="https://predannoeserdce.ru/catalog/",
    ),
    "попечительская программа": LinkButtonAttributes(
        text="Целевая страница для участия в Попечительской программе",
        url="https://predannoeserdce.ru/programmy-prijuta/popechitelstvo/",
    ),
}
MENU_LAYOUT = 3
FAQ_PER_PAGE = 5


# Отдельные кнопки
class OneButtonItems:
    MENU = "главное меню"
    CANCEL = "⬅️ назад в меню"
    RETURN = "попробовать еще раз"


# Задержки
START_SLEEP = 1
MENU_SLEEP = 3

# ---- Данные с сервера ---- #

# Получение и обновление списка вопросов
SERVER_API_FAQ_URL = os.getenv(key="SERVER_API_FAQ_URL")
FAQ_UPDATE_INTERVAL_MINUTES = 10

# Токен
SERVER_API_TOKEN_URL = os.getenv(key="SERVER_API_TOKEN_URL")
TOKEN_UPDATE_HOURS = 12

# Подписка
SERVER_API_CUSTOMER_URL = os.getenv(key="SERVER_API_CUSTOMER_URL")


# Проверки введенного текста
class RegexText:
    USER_FULLNAME = r"(\b[А-ЯЁ]{1}[а-яё]+\b)"
    EMAIL = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    PHONE = r"^[7|8]\d{10}$"


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
    TG_QUESTION = "tg_question"
    EMAIL_QUESTION = "email_question"
    BACK_TO_CATEGORIES = "back_to_categories"
    BACK_TO_FAQ = "back_to_faq"
    SERVER_ERROR = "server_error"
    USER_TO_BAN = "user_to_ban"


# Настройки логгера:
class LogSetting:
    FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LEVEL = logging.INFO
    NAME = "tg_bot"
    FILENAME = "bot_logs/tg_bot.log"
    ENCODING = "utf8"
    FILESIZE = 1024 * 1024
    FILECOUNT = 3


# Черный список
class BanList:
    FILENAME = "bot_ban/blacklist.txt"
    ENCODING = "utf8"


# Рабочее время администратора
class AdminWorkTime:
    START_H = 10
    START_MIN = 0
    END_H = 20
    END_MIN = 0
    TIMEZONE = "Europe/Moscow"


# Отложенные сообщения для администратора
class DelayedQuestionsAttr:
    FILENAME = "delayed_qstns.txt"
    ENCODING = "utf8"
    MSG_SEPARATOR = "\n__!РАЗДЕЛИТЕЛЬ!__\n"


class DelayedQuestionsSendDelay:
    MINIMUM = 2
    MAXIMUM = 7


# Изображение кота Фуражкина
MASCOT_FILENAME = "assets/bgfooter_kot.png"
