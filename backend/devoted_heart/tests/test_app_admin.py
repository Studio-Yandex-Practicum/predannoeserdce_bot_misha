from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from unittest.mock import patch
from tempfile import NamedTemporaryFile


from app.admin import FAQAdmin, CustomerAdmin, MessagesAdmin
from app.models import FAQ, Customer, Messages


class FAQAdminTest(TestCase):

    def test_list_display(self):
        faq_admin = FAQAdmin(FAQ, None)
        self.assertEqual(
            faq_admin.list_display,
            ('pk', 'question', 'answer', 'category', 'order')
        )


class CustomerAdminTest(TestCase):

    def test_list_display(self):
        customer_admin = CustomerAdmin(Customer, None)
        self.assertEqual(
            customer_admin.list_display,
            ('pk', 'name', 'email', 'tg_id', 'phone', 'registration_date')
        )


class MessagesAdminTest(TestCase):

    def test_list_display(self):
        messages_admin = MessagesAdmin(Messages, None)
        self.assertEqual(
            messages_admin.list_display,
            ('text', 'display_image', 'selected')
        )

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='admin', password='admin123', is_staff=True
        )
        with NamedTemporaryFile(suffix=".jpg", delete=False) as temp_image:
            temp_image.write(b"Some image data")
            temp_image.flush()

            self.message = Messages.objects.create(
                text='Test Message', image=temp_image.name, selected=False
            )

    @patch('app.regular_messages.ThreadPoolExecutor')
    def test_send_messages_view(self, mock_executor):
        mock_executor.return_value.submit.return_value.result.return_value = None  # noqa
        selected_messages = Messages.objects.create(  # noqa
            text='Selected Message 1', selected=True
        )
        self.client.login(username='admin', password='admin123')
        url = reverse('admin:send_messages')
        data = {
            'action': 'send_messages_view',
            '_selected_action': [str(self.message.id)]
        }

        response = self.client.post(url, data, follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertIn(
            'Сообщения успешно отправлены подписчикам.'.encode('utf-8'),
            response.content
        )

    @patch('app.regular_messages.ThreadPoolExecutor')
    @patch('app.models.SchedulerSettings.objects.first')
    def test_start_scheduler(self, mock_settings, mock_executor):
        self.client.login(username='admin', password='admin123')
        mock_settings.return_value.scheduler_period = 60
        mock_executor.return_value.submit.return_value.result.return_value = None  # noqa
        url = reverse('admin:start_scheduler')
        data = {
            'action': 'start_scheduler',
            '_selected_action': [str(self.message.id)]
        }

        response = self.client.post(url, data, follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertIn(
            'Планировщик успешно запущен.'.encode('utf-8'), response.content
        )

    def test_stop_scheduler(self):
        self.client.login(username='admin', password='admin123')

        url = reverse('admin:stop_scheduler')
        data = {
            'action': 'stop_scheduler',
            '_selected_action': [str(self.message.id)]
        }

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertIn(
            'Планировщик успешно остановлен.'.encode('utf-8'), response.content
        )
