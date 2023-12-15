import logging

from constants import LOGGING_LEVEL

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=LOGGING_LEVEL,
)
bot_logger = logging.getLogger(name="tg_bot")
