from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class TokenViewsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@test.com", password="pass")  # type: ignore
        self.obtain_url = reverse("users:token_obtain_pair")
        self.refresh_url = reverse("users:token_refresh")

    def test_valid_credentials(self):
        response = self.client.post(
            self.obtain_url, {"email": "test@test.com", "password": "pass"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get("access"))
        self.assertIsNotNone(response.data.get("refresh"))

    def test_invalid_credentials(self):
        response = self.client.post(
            self.obtain_url, {"email": "test@test.com", "password": "uwu"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsNone(response.data.get("access"))
        self.assertIsNone(response.data.get("refresh"))

    def test_valid_token_refreshing(self):
        response = self.client.post(
            self.obtain_url, {"email": "test@test.com", "password": "pass"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get("access"))
        self.assertIsNotNone(refresh_token := response.data.get("refresh"))

        response = self.client.post(self.refresh_url, {"refresh": refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get("access"))

    def test_invalid_token_refreshing(self):
        response = self.client.post(self.refresh_url, {"refresh": "fake token"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsNone(response.data.get("access"))
