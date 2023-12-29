EMPTY_FIELD_VALUE = '-пусто-'
JWT_TOKEN_FILE_DAYS = 1
DEFAULT_PAGE_SIZE = 10

LIMIT_VALUE_TEXT = 2046

SCHEDULER_DEFAULT = 60
MAX_SCHEDULER_PERIOD = 2592000
MIN_SCHEDULER_PERIOD = 60
MAX_SCHEDULER_MESSAGE = (
    'Убедитесь, что период рассылки не превышает 1 месяц(2592000 сек)'
)
MIN_SCHEDULER_MESSAGE = (
    'Убедитесь, что период рассылки не меньше 60 сек.'
)


class ApiEnabled:
    ENABLE_USERS = False
    ENABLE_FAQ = True
    ENABLE_CUSTOMER = True
