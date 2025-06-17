from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Course, Lesson

User = get_user_model()


class CourseViewsTests(APITestCase):
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
        self.assertEqual(self.course_owned.title, "Owner Course")

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

    # SUBSCRIPTION
    def test_course_subscription_endpoint(self):
        self.authenticate(self.owner)
        url = reverse("materials:course-subscription", args=[self.course_owned.id])

        # subscribe
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course_owned.refresh_from_db()
        self.assertTrue(self.course_owned.subscriptions.exists())

        # unsubscribe back
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course_owned.refresh_from_db()
        self.assertFalse(self.course_owned.subscriptions.exists())

    def test_course_subscription_endpoint_as_unauthenticated(self):
        url = reverse("materials:course-subscription", args=[self.course_owned.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.course_owned.refresh_from_db()
        self.assertFalse(self.course_owned.subscriptions.exists())


class LessonViewsTests(APITestCase):
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

        # courses and lessons
        self.course_owned = Course.objects.create(
            title="Owner Course", owner=self.owner
        )
        self.lesson_owned = Lesson.objects.create(
            title="Owner Lesson",
            owner=self.owner,
            video_url="https://youtube.com",
            course=self.course_owned,
        )

        self.course_other = Course.objects.create(
            title="Other Course", owner=self.other_user
        )
        self.lesson_other = Lesson.objects.create(
            title="Other Lesson", owner=self.other_user, course=self.course_other
        )

        self.list_url = reverse("materials:lesson-list")

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    # LIST
    def test_list_lessons_as_owner(self):
        self.authenticate(self.owner)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_list_lessons_as_moderator(self):
        self.authenticate(self.moderator)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # should see all lessons
        self.assertEqual(len(response.data["results"]), 2)

    def test_list_lessons_as_unauthenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsNone(response.data.get("results"))

    # CREATE
    def test_create_lesson_with_own_course(self):
        self.authenticate(self.owner)
        response = self.client.post(
            self.list_url,
            {
                "title": "Test Title",
                "video_url": "https://youtube.com",
                "course": self.course_owned.id,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.last().owner, self.owner)

    def test_create_lesson_with_wrong_video_url(self):
        self.authenticate(self.owner)
        response = self.client.post(
            self.list_url,
            {
                "title": "Test Title",
                "video_url": "https://UwU.com",
                "course": self.course_owned.id,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(Lesson.objects.last().owner, self.owner)

    def test_create_lesson_with_foreign_course(self):
        self.authenticate(self.owner)
        response = self.client.post(
            self.list_url,
            {
                "title": "Test Title",
                "video_url": "https://youtube.com",
                "course": self.course_other.id,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(Lesson.objects.last().owner, self.owner)

    def test_create_lesson_as_moderator(self):
        self.authenticate(self.moderator)
        response = self.client.post(
            self.list_url,
            {
                "title": "Test Title",
                "video_url": "https://youtube.com",
                "course": self.course_owned.id,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_lesson_as_unauthenticated(self):
        response = self.client.post(
            self.list_url,
            {
                "title": "Test Title",
                "video_url": "https://youtube.com",
                "course": self.course_owned.id,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # RETRIEVE
    def test_retrieve_lesson_as_owner(self):
        self.authenticate(self.owner)
        url = reverse("materials:lesson-detail", args=[self.lesson_owned.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_lesson_as_moderator(self):
        self.authenticate(self.moderator)
        url = reverse("materials:lesson-detail", args=[self.lesson_owned.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_lesson_as_unauthenticated(self):
        url = reverse("materials:lesson-detail", args=[self.lesson_owned.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_lesson_as_random_user(self):
        self.authenticate(self.other_user)
        url = reverse("materials:lesson-detail", args=[self.lesson_owned.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # UPDATE
    def test_update_lesson_as_owner(self):
        self.authenticate(self.owner)
        url = reverse("materials:lesson-detail", args=[self.lesson_owned.id])
        response = self.client.patch(url, {"title": "UPDATED"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson_owned.refresh_from_db()
        self.assertEqual(self.lesson_owned.title, "UPDATED")

    def test_update_lesson_as_moderator(self):
        self.authenticate(self.moderator)
        url = reverse("materials:lesson-detail", args=[self.lesson_owned.id])
        response = self.client.patch(url, {"title": "UPDATED"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson_owned.refresh_from_db()
        self.assertEqual(self.lesson_owned.title, "UPDATED")

    def test_update_lesson_as_unauthenticated(self):
        url = reverse("materials:lesson-detail", args=[self.lesson_owned.id])
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_lesson_as_random_user(self):
        self.authenticate(self.other_user)
        url = reverse("materials:lesson-detail", args=[self.lesson_owned.id])
        response = self.client.patch(url, {"title": "UPDATED"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.lesson_owned.refresh_from_db()
        self.assertEqual(self.lesson_owned.title, "Owner Lesson")

    # DESTROY
    def test_destroy_lesson_as_owner(self):
        self.authenticate(self.owner)
        url = reverse("materials:lesson-detail", args=[self.lesson_owned.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_destroy_lesson_as_moderator(self):
        self.authenticate(self.moderator)
        url = reverse("materials:lesson-detail", args=[self.lesson_owned.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_lessons_as_unauthenticated(self):
        url = reverse("materials:lesson-detail", args=[self.lesson_owned.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_destroy_lesson_as_random_user(self):
        self.authenticate(self.other_user)
        url = reverse("materials:lesson-detail", args=[self.lesson_owned.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
