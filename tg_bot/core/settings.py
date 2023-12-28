import logging
from logging.handlers import RotatingFileHandler

from core.constants import LogSetting

logging.basicConfig(
    format=LogSetting.FORMAT,
    level=LogSetting.LEVEL,
)
bot_logger = logging.getLogger(name=LogSetting.NAME)
bot_handler = RotatingFileHandler(
    filename=LogSetting.FILENAME,
    encoding=LogSetting.ENCODING,
    maxBytes=LogSetting.FILESIZE,
    backupCount=LogSetting.FILECOUNT,
)
bot_handler.setLevel(level=LogSetting.LEVEL)
formatter = logging.Formatter(fmt=LogSetting.FORMAT)
bot_handler.setFormatter(fmt=formatter)
bot_logger.addHandler(hdlr=bot_handler)
