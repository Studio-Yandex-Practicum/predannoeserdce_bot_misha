from django.test import TestCase  # RequestFactory
from app.admin import FAQAdmin, CustomerAdmin, MessagesAdmin
from app.models import FAQ, Customer, Messages
from django.contrib.auth import get_user_model
from django.urls import reverse


class FAQAdminTest(TestCase):

    def test_list_display(self):
        faq_admin = FAQAdmin(FAQ, None)
        self.assertEqual(faq_admin.list_display, ('pk', 'question', 'order'))


class CustomerAdminTest(TestCase):

    def test_list_display(self):
        customer_admin = CustomerAdmin(Customer, None)
        self.assertEqual(
            customer_admin.list_display,
            ('pk', 'name', 'email', 'tg_id', 'phone')
        )


class MessagesAdminTest(TestCase):

    def test_list_display(self):
        messages_admin = MessagesAdmin(Messages, None)
        self.assertEqual(
            messages_admin.list_display,
            ('text', 'image', 'selected')
        )

    def setUp(self):
        # Создаем пользователя для входа в админку
        User = get_user_model()  # в тесте ушли от модели юзерс
        self.user = User.objects.create_user(
            username='admin', password='admin123', is_staff=True
        )
        # Создаем объекты для тестирования
        self.message = Messages.objects.create(
            text='Test Message', image=None, selected=False
        )

    def test_send_messages_view(self):
        # Аутентификация пользователя
        self.client.login(username='admin', password='admin123')

        # Подготовка URL и данных для отправки запроса
        url = reverse('admin:send_messages')
        data = {
            'action': 'send_messages_view',
            '_selected_action': [str(self.message.id)]
        }

        # Отправка POST-запроса для выполнения действия
        response = self.client.post(url, data, follow=True)

        # Проверка успешного выполнения
        self.assertEqual(response.status_code, 200)

        # Проверка того, что сообщение отправлено
        self.assertIn(
            'Сообщения успешно отправлены подписчикам.'.encode('utf-8'),
            response.content
        )

    def test_start_scheduler(self):
        # Аутентификация пользователя
        self.client.login(username='admin', password='admin123')

        # Подготовка URL и данных для отправки запроса
        url = reverse('admin:start_scheduler')
        data = {
            'action': 'start_scheduler',
            '_selected_action': [str(self.message.id)]
        }

        # Отправка POST-запроса для выполнения действия
        response = self.client.post(url, data, follow=True)

        # Проверка успешного выполнения
        self.assertEqual(response.status_code, 200)

        # Проверка того, что планировщик успешно запущен
        self.assertIn(
            'Планировщик успешно запущен.'.encode('utf-8'), response.content
        )

    def test_stop_scheduler(self):
        # Аутентификация пользователя
        self.client.login(username='admin', password='admin123')

        # Подготовка URL и данных для отправки запроса
        url = reverse('admin:stop_scheduler')
        data = {
            'action': 'stop_scheduler',
            '_selected_action': [str(self.message.id)]
        }

        # Отправка POST-запроса для выполнения действия
        response = self.client.post(url, data, follow=True)

        # Проверка успешного выполнения
        self.assertEqual(response.status_code, 200)

        # Проверка того, что планировщик успешно остановлен
        self.assertIn(
            'Планировщик успешно остановлен.'.encode('utf-8'), response.content
        )
