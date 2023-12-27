from unittest.mock import AsyncMock, Mock

import pytest
from django.conf import settings
from telegram import InlineKeyboardButton


@pytest.fixture
def update():
    """Update object fixture for telegram handlers."""
    return AsyncMock()


@pytest.fixture
def context():
    """Context object fixture for telegram handlers."""
    context = AsyncMock()
    context.bot = AsyncMock()
    context.bot.set_my_commands = AsyncMock(return_value=[])
    context.bot.set_chat_menu_button = AsyncMock(return_value=[])
    return context


@pytest.fixture
def mocked_reply_markup():
    """Reply markup mock."""
    return AsyncMock(return_value=[])


@pytest.fixture
def mocked_message_text():
    """Message text mock."""
    return "MESSAGE"


@pytest.fixture
def mocked_message(mocked_message_text):
    """Message object mock."""
    message = Mock()
    message.text = mocked_message_text
    return message


@pytest.fixture
def async_mocked_reply_markup():
    """Message object mock."""
    return AsyncMock(return_value=[])

@pytest.fixture
def mocked_pagination_reply_markup():
    """Reply markup pagination."""
    return '{"inline_keyboard": [[{"callback_data": "profession_prof-1", "text": "prof-1"}]]}'
