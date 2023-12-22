from http import HTTPStatus

import requests
from requests import Response

from constants import SERVER_API_FAQ_URL, MainCallbacks
from message_config import MESSAGES, MenuLogMessage
from settings import bot_logger


def get_faq() -> list[dict[str, str | int]]:
    """Получение из БД списка частых вопросов и ответов."""
    url = SERVER_API_FAQ_URL
    results = []
    while True:
        try:
            response: Response = requests.get(url=url)
        except Exception as error:
            bot_logger.error(msg=MenuLogMessage.UNKNOWN_ERROR % (error,))
        if response.status_code != HTTPStatus.OK:
            bot_logger.error(
                msg=MenuLogMessage.SERVER_ERROR % (response.status_code,)
            )
            return [
                {
                    "question": MESSAGES["server_error"],
                    "order": MainCallbacks.SERVER_ERROR,
                }
            ]
        data = response.json()
        results += data["results"]
        if not data["next"]:
            break
        url = data["next"]
    bot_logger.info(msg=MenuLogMessage.UPDATE_FAQ_LIST)
    return results
