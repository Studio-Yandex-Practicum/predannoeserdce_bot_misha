import logging

from constants import LOGGING_LEVEL

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=LOGGING_LEVEL,
)
logger = logging.getLogger(name="TG_BOT")
