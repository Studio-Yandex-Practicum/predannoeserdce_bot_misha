from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # создаем юзер модель для тестов
        User = get_user_model()

        # создадим юзера для аутентификации
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        self.client.force_authenticate(user=self.user)

    def test_customer_viewset_list(self):
        response = self.client.get('/api/customer/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_faq_list(self):
        response = self.client.get('/api/faq/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
