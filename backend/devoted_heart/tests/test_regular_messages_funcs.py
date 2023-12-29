import unittest
from unittest.mock import patch
from django.test import TestCase
from app.regular_messages import (
    send_regular_message, get_chat_ids, get_random_text,
    get_random_positive_thought, get_random_cat_image,
    get_random_dog_image
)


class RegularMessagesTestCase(TestCase):
    def setUp(self):
        self.chat_ids = ['123', '456', '789']

    @patch('app.regular_messages.Customer.objects.all')
    def test_get_chat_ids_success(self, mock_customer_all):
        mock_customer_all.return_value.values_list.return_value = self.chat_ids
        result = get_chat_ids()
        self.assertEqual(result, self.chat_ids)

    @patch('app.regular_messages.Customer.objects.all')
    @patch('app.regular_messages.logger.error')
    def test_get_chat_ids_exception(
        self, mock_logger_error, mock_customer_all
    ):
        mock_customer_all.side_effect = Exception('Test error')
        result = get_chat_ids()
        self.assertEqual(result, [])
        mock_logger_error.assert_called_once()

    @patch('telebot.TeleBot.send_message')
    def test_send_regular_message(self, mock_send_message):
        chat_id = 123
        message_content = "Test message"
        send_regular_message(chat_id, message_content)
        mock_send_message.assert_any_call(chat_id, message_content)

    def test_get_random_text(self):
        text = get_random_text()
        self.assertIsNotNone(text)

    def test_get_random_positive_thought(self):
        thought = get_random_positive_thought()
        self.assertIsNotNone(thought)

    def test_get_random_cat_image(self):
        cat_image = get_random_cat_image()
        self.assertIsNotNone(cat_image)

    def test_get_random_dog_image(self):
        dog_image = get_random_dog_image()
        self.assertIsNotNone(dog_image)


if __name__ == '__main__':
    unittest.main()
