import logging
import os

from dotenv import load_dotenv

from utils import LinkButtonAttributes

load_dotenv()

# Константы для телеграма
TELEGRAM_TOKEN = os.getenv(key="TELEGRAM_TOKEN")
ADMIN_CHAT_ID = os.getenv(key="ADMIN_CHAT_ID")

# Уровень логгера
LOGGING_LEVEL = logging.INFO

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
}
MENU_LAYOUT = 3
FAQ_PER_PAGE = 5

# Задержки
START_SLEEP = 1
MENU_SLEEP = 3

# Получение и обновление списка вопросов
SERVER_API_FAQ_URL = os.getenv(key="SERVER_API_FAQ_URL")
FAQ_UPDATE_INTERVAL_MINUTES = 10
