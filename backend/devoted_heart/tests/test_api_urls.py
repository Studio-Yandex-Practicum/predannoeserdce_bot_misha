from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class NON_AUTH_UrlsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_non_auth_urls(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/faq/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/customer/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AUTH_UrlsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # модель для тестов
        User = get_user_model()

        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='testpassword'
        )
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/auth/token/login/')
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

        response = self.client.get('/api/auth/token/logout/')
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

        response = self.client.get('/api/customer/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
