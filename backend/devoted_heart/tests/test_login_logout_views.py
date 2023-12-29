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
        """Тест login view"""
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
        """
        Тест logout view.
        До logout user должен пройти аутентификацию и
        получить токен.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            '/api/auth/token/login/',
            {'email': 'testuser@example.com', 'password': 'testpassword'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('auth_token')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.post('/api/auth/token/logout/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
