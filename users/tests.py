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

    # OBTAIN
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

    # REFRESH
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


class UserViewsTests(APITestCase):
    def setUp(self) -> None:
        self.main_user = User.objects.create_user(  # type: ignore
            email="main@main.com",
            first_name="Firstname",
            last_name="Lastname",
            password="pass",
        )
        self.other_user = User.objects.create_user(  # type: ignore
            email="other@other.com",
            password="pass",
        )

        self.register_url = reverse("users:register")

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    # REGISTRATION
    def test_registration_successful(self):
        request = self.client.post(
            self.register_url, {"email": "test@test.com", "password": "pass"}
        )
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.last().email, "test@test.com")

    def test_registration_email_exists(self):
        request = self.client.post(
            self.register_url, {"email": "main@main.com", "password": "pass"}
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 2)

    # RETRIEVE
    def test_retrieve_self(self):
        self.authenticate(self.main_user)

        detail_url = reverse("users:user-detail", args=[self.main_user.id])
        request = self.client.get(detail_url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(request.data.get("last_name"))
        self.assertIsNotNone(request.data.get("payments"))

    def test_retrieve_foreign(self):
        self.authenticate(self.other_user)

        detail_url = reverse("users:user-detail", args=[self.main_user.id])
        request = self.client.get(detail_url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertIsNone(request.data.get("last_name"))
        self.assertIsNone(request.data.get("payments"))

    def test_retrieve_as_unauthorized(self):
        detail_url = reverse("users:user-detail", args=[self.main_user.id])
        request = self.client.get(detail_url)
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_non_existent_user(self):
        self.authenticate(self.main_user)

        detail_url = reverse("users:user-detail", args=[0])
        request = self.client.get(detail_url)
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

    # UPDATE
    def test_update_self(self):
        self.authenticate(self.main_user)

        detail_url = reverse("users:user-detail", args=[self.main_user.id])
        request = self.client.patch(detail_url, {"last_name": "UPDATED"})
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.main_user.refresh_from_db()
        self.assertEqual(self.main_user.last_name, "UPDATED")

    def test_update_foreign(self):
        self.authenticate(self.main_user)

        detail_url = reverse("users:user-detail", args=[self.other_user.id])
        request = self.client.patch(detail_url, {"last_name": "UPDATED"})
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)
        self.other_user.refresh_from_db()
        self.assertNotEqual(self.other_user.last_name, "UPDATED")

    # DESTROY
    def test_destroy_self(self):
        self.authenticate(self.main_user)

        detail_url = reverse("users:user-detail", args=[self.main_user.id])
        request = self.client.delete(detail_url)
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)

    def test_destroy_foreign(self):
        self.authenticate(self.main_user)

        detail_url = reverse("users:user-detail", args=[self.other_user.id])
        request = self.client.delete(detail_url)
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)
        self.other_user.refresh_from_db()
        self.assertTrue(self.other_user)
