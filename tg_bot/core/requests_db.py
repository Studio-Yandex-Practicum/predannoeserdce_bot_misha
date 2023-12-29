import os
from http import HTTPStatus

import requests
from requests import Response

from core.constants import (
    ADMIN_LOGIN,
    ADMIN_PASSWORD,
    SERVER_API_CUSTOMER_URL,
    SERVER_API_FAQ_URL,
    SERVER_API_TOKEN_URL,
)
from core.message_config import BotLogMessage, MainMessage
from core.settings import bot_logger


def get_faq() -> dict[str | int, str]:
    """Получение из БД списка частых вопросов и ответов."""
    url = SERVER_API_FAQ_URL
    results = {}
    while True:
        try:
            response: Response = requests.get(url=url)
        except Exception as error:
            bot_logger.error(msg=BotLogMessage.UNKNOWN_ERROR % error)
        if response.status_code != HTTPStatus.OK:
            bot_logger.error(
                msg=BotLogMessage.SERVER_ERROR % (response.status_code,)
            )
            results.update({MainMessage.SERVER_ERROR: ""})
            return results
        data = response.json()
        results.update(data["results"])
        if not data["next"]:
            break
        url = data["next"]
    bot_logger.info(msg=BotLogMessage.UPDATE_FAQ_DICT)
    return results


def get_headers(token) -> dict[str, str]:
    """Подготавливает заголовок."""
    return {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json",
    }


def get_token() -> None:
    """Получение токена для бота."""
    token_url = SERVER_API_TOKEN_URL
    credentials = {"email": ADMIN_LOGIN, "password": ADMIN_PASSWORD}
    try:
        response = requests.post(url=token_url, data=credentials)
    except Exception as error:
        bot_logger.error(msg=BotLogMessage.UNKNOWN_ERROR % error)
    if response.status_code != HTTPStatus.OK:
        bot_logger.error(
            msg=BotLogMessage.SERVER_ERROR % (response.status_code,)
        )
        return None
    token_data = response.json()
    token = token_data.get("auth_token")
    os.environ["ADMIN_TOKEN"] = token
    bot_logger.info(msg=BotLogMessage.TOKEN_RECEIVED)


def check_subscribe(user_id) -> Response:
    """Проверка подписки пользователем на рассылку."""
    subscribe_url = f"{SERVER_API_CUSTOMER_URL}{user_id}"
    token = os.getenv(key="ADMIN_TOKEN")
    try:
        response = requests.get(
            url=subscribe_url,
            headers=get_headers(token=token),
        )
    except Exception as error:
        bot_logger.error(msg=BotLogMessage.UNKNOWN_ERROR % error)
        return None
    return response


def delete_subscriber(user_id) -> Response:
    """Удаление пользователя из таблицы клиентов."""
    subscribe_url = f"{SERVER_API_CUSTOMER_URL}{user_id}"
    token = os.getenv(key="ADMIN_TOKEN")
    try:
        response = requests.delete(
            url=subscribe_url,
            headers=get_headers(token=token),
        )
    except Exception as error:
        bot_logger.error(msg=BotLogMessage.UNKNOWN_ERROR % error)
        return None
    return response
