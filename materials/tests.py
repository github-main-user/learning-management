from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


from .models import Course


class CourseViewSetTests(APITestCase):
    def setUp(self):
        # groups
        self.moderators_group = Group.objects.create(name="moderators")

        # users
        self.owner = User.objects.create_user(email="owner@owner.com", password="pass")  # type: ignore
        self.moderator = User.objects.create_user(  # type: ignore
            email="moder@model.com", password="pass"
        )
        self.moderator.groups.add(self.moderators_group)
        self.other_user = User.objects.create_user(  # type: ignore
            email="other@other.com", password="pass"
        )

        # courses
        self.course_owned = Course.objects.create(
            title="Owner Course", owner=self.owner
        )
        self.course_other = Course.objects.create(
            title="Other Course", owner=self.other_user
        )

        self.list_url = reverse("materials:course-list")

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    # LIST
    def test_list_courses_as_owner(self):
        self.authenticate(self.owner)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_list_courses_as_moderator(self):
        self.authenticate(self.moderator)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # should see all courses
        self.assertEqual(len(response.data["results"]), 2)

    def test_list_courses_as_unauthenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsNone(response.data.get("results"))

    # CREATE
    def test_create_course_as_owner(self):
        self.authenticate(self.owner)
        response = self.client.post(self.list_url, {"title": "Test Title"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.last().owner, self.owner)

    def test_create_course_as_moderator(self):
        self.authenticate(self.moderator)
        response = self.client.post(self.list_url, {"title": "Test Title"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_course_as_unauthenticated(self):
        response = self.client.post(self.list_url, {"title": "Test Title"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # RETRIEVE
    def test_retrieve_course_as_owner(self):
        self.authenticate(self.owner)
        url = reverse("materials:course-detail", args=[self.course_owned.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_course_as_moderator(self):
        self.authenticate(self.moderator)
        url = reverse("materials:course-detail", args=[self.course_owned.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_course_as_unauthenticated(self):
        url = reverse("materials:course-detail", args=[self.course_owned.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_course_as_random_user(self):
        self.authenticate(self.other_user)
        url = reverse("materials:course-detail", args=[self.course_owned.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # UPDATE
    def test_update_course_as_owner(self):
        self.authenticate(self.owner)
        url = reverse("materials:course-detail", args=[self.course_owned.id])
        response = self.client.patch(url, {"title": "UPDATED"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course_owned.refresh_from_db()
        self.assertEqual(self.course_owned.title, "UPDATED")

    def test_update_course_as_moderator(self):
        self.authenticate(self.moderator)
        url = reverse("materials:course-detail", args=[self.course_owned.id])
        response = self.client.patch(url, {"title": "UPDATED"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course_owned.refresh_from_db()
        self.assertEqual(self.course_owned.title, "UPDATED")

    def test_update_course_as_unauthenticated(self):
        url = reverse("materials:course-detail", args=[self.course_owned.id])
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_course_as_random_user(self):
        self.authenticate(self.other_user)
        url = reverse("materials:course-detail", args=[self.course_owned.id])
        response = self.client.patch(url, {"title": "UPDATED"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.course_owned.refresh_from_db()
        self.assertEqual(self.course_owned.title, self.course_owned.title)

    # DESTROY
    def test_destroy_course_as_owner(self):
        self.authenticate(self.owner)
        url = reverse("materials:course-detail", args=[self.course_owned.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_destroy_course_as_moderator(self):
        self.authenticate(self.moderator)
        url = reverse("materials:course-detail", args=[self.course_owned.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_courses_as_unauthenticated(self):
        url = reverse("materials:course-detail", args=[self.course_owned.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_destroy_course_as_random_user(self):
        self.authenticate(self.other_user)
        url = reverse("materials:course-detail", args=[self.course_owned.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
