from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # отдельная модель для тестирования
        User = get_user_model()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='testpassword'
        )

    def test_custom_login_view(self):
        response = self.client.post(
            '/api/auth/token/login/',
            {
                'email': 'testuser@example.com',
                'username': 'testuser',
                'password': 'testpassword'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_custom_logout_view(self):
        pass
