import unittest
from django.test import TestCase
from unittest.mock import patch, call, mock_open
from app.regular_messages import (
    send_regular_message, send_messages, send_photo, send_schedular_messages
)
from app.models import Messages


class RegularMessagesTestCase(TestCase):
    def setUp(self):
        pass

    @patch('app.regular_messages.bot.send_message')
    @patch('app.regular_messages.bot.send_photo')
    @patch('app.regular_messages.random.choice')
    @patch('app.regular_messages.get_random_text')
    @patch('app.regular_messages.get_random_cat_image')
    @patch('app.regular_messages.get_random_dog_image')
    @patch('app.regular_messages.get_random_positive_thought')
    @patch('app.regular_messages.get_chat_ids')
    def test_send_regular_message(
        self, mock_get_chat_ids, mock_get_positive_thought,
        mock_get_dog_image, mock_get_cat_image, mock_get_text,
        mock_random_choice, mock_send_photo, mock_send_message
    ):
        """
        Тест рассылки регулярного сообщения с/без сообщения администратора
        """
        chat_id = 123
        message_content = 'Test Message'
        mock_get_chat_ids.return_value = [chat_id]
        mock_get_text.return_value = 'Random Text'
        mock_get_cat_image.return_value = 'Cat Image URL'
        mock_get_dog_image.return_value = 'Dog Image URL'
        mock_get_positive_thought.return_value = 'Positive Thought'
        mock_random_choice.return_value = 1

        send_regular_message(chat_id, message_content)
        calls = [call(chat_id, message_content)]
        calls.extend([call(chat_id, 'Random Text')])
        mock_send_message.assert_has_calls(calls)

        mock_get_text.reset_mock()
        mock_random_choice.return_value = 2
        send_regular_message(chat_id,)
        calls = []
        calls.extend([call(chat_id, 'Cat Image URL')])
        mock_send_photo.assert_has_calls(calls)

    @patch('app.regular_messages.bot.send_message')
    @patch('app.regular_messages.bot.send_photo')
    @patch('app.regular_messages.get_chat_ids')
    def test_send_messages(
        self, mock_get_chat_ids, mock_send_photo, mock_send_message
    ):
        """Тест рассылки сообщений по списку клиентов"""
        message = Messages(text='Text 1')
        selected_messages = [message,]

        mock_get_chat_ids.return_value = [123, 321]

        send_messages(selected_messages)
        calls = [call(123, message.text)]
        calls.extend([call(321, message.text)])

        mock_send_message.assert_has_calls(calls)

    @patch('app.regular_messages.bot.send_message')
    @patch('app.regular_messages.bot.send_photo')
    @patch('app.regular_messages.random.choice')
    @patch('app.regular_messages.get_random_text')
    @patch('app.regular_messages.get_random_cat_image')
    @patch('app.regular_messages.get_random_dog_image')
    @patch('app.regular_messages.get_random_positive_thought')
    @patch('app.regular_messages.get_chat_ids')
    def test_send_schedular_messages(
        self, mock_get_chat_ids, mock_get_positive_thought,
        mock_get_dog_image, mock_get_cat_image, mock_get_text,
        mock_random_choice, mock_send_photo, mock_send_message
    ):
        """Тесты рассылки сообщений планировщиком"""
        selected_message_1 = Messages.objects.create(  # noqa
            text='Selected Message 1', selected=True
        )
        mock_get_chat_ids.return_value = [123, 321]
        mock_get_text.return_value = 'Random Text'
        mock_get_cat_image.return_value = 'Cat Image URL'
        mock_get_dog_image.return_value = 'Dog Image URL'
        mock_get_positive_thought.return_value = 'Positive Thought'
        mock_random_choice.return_value = 1

        send_schedular_messages()

        calls = [call(123, 'Selected Message 1'), call(123, 'Random Text')]
        calls.extend(
            [call(321, 'Selected Message 1'), call(321, 'Random Text')]
        )
        mock_send_message.assert_has_calls(calls)

    @patch('app.regular_messages.bot')
    def test_send_photo_success(self, mock_bot):
        chat_id = 123
        image_path = 'test.jpg'
        open_mock = mock_open()

        with patch('builtins.open', open_mock):
            send_photo(chat_id, image_path)

        open_mock.assert_called_once_with(image_path, 'rb')
        mock_bot.send_photo.assert_called_once_with(
            chat_id, open_mock.return_value
        )

    @patch('app.regular_messages.bot')
    @patch('app.regular_messages.logger')
    def test_send_photo_failure(self, mock_logger, mock_bot):
        chat_id = 123
        image_path = 'test.jpg'
        open_mock = mock_open()
        exception_message = 'Some error'

        with patch('builtins.open', open_mock):
            mock_bot.send_photo.side_effect = Exception(exception_message)
            send_photo(chat_id, image_path)

        open_mock.assert_called_once_with(image_path, 'rb')
        mock_bot.send_photo.assert_called_once_with(
            chat_id, open_mock.return_value
        )
        mock_logger.error.assert_called_once_with(
            f'Ошибка с отправкой изображения на {chat_id}: {exception_message}'
        )


if __name__ == '__main__':
    unittest.main()
