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
    "Частые вопросы": "faq",
    "Подписаться на рассылку": "subscribe",
}
LINK_ITEMS: dict[str, LinkButtonAttributes] = {
    "Попечительство": LinkButtonAttributes(
        text="Условия попечительства можно посмотреть на сайте",
        url="https://predannoeserdce.ru/programmy-prijuta/popechitelstvo/",
    ),
    "Пожертвование": LinkButtonAttributes(
        text="Сделать пожертвование можно перейдя по ссылке",
        url="https://predannoeserdce.ru/help/",
    ),
    "Взять котика": LinkButtonAttributes(
        text="Взять котика домой можно по ссылке",
        url="https://predannoeserdce.ru/howtohelp/take-home/",
    ),
    "Посмотреть котиков": LinkButtonAttributes(
        text="Посмотреть котиков можно по ссылке",
        url="https://predannoeserdce.ru/catalog-opeka/",
    ),
}
MENU_LAYOUT = 3

# Задержки
START_SLEEP = 3
MENU_SLEEP = 5

# Получение и обновление списка вопросов
SERVER_API_FAQ_URL = os.getenv(key="SERVER_API_FAQ_URL")
MINUTES_FAQ_UPDATE_INTERVAL = 10
