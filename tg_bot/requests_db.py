from http import HTTPStatus

import requests
from requests import Response

from constants import SERVER_API_FAQ_URL
from message_config import LogMessage
from settings import bot_logger


def get_faq() -> dict:
    url = SERVER_API_FAQ_URL
    results = []
    while True:
        try:
            response: Response = requests.get(url=url)
        except Exception as error:
            bot_logger.error(msg=LogMessage.UNKNOWN_ERROR % (error,))
        if response.status_code != HTTPStatus.OK:
            bot_logger.error(
                msg=LogMessage.SERVER_ERROR % (response.status_code,)
            )
            return {
                "Ошибка. Нажмите, "
                "чтобы сообщить администратору": "server_error"
            }
        data = response.json()
        results += data["results"]
        if not data["next"]:
            break
        url = data["next"]
    return results
