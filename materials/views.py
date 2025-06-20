from datetime import timedelta
from typing import override

from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.paginators import MaterialsPaginator
from users.permissions import IsModerator, IsOwner

from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer
from .tasks import notify_about_course_update


class CourseSubscriptionAPIView(APIView):
    """Handles User Subscription to a Course."""

    def post(self, request, pk: int):
        user = request.user

        course = get_object_or_404(Course, pk=pk)
        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = "User unsubscribed"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "User successfully subscribed"

        return Response({"message": message})


class CourseViewAPISet(viewsets.ModelViewSet):
    """
    ViewSet for Course model.

    Returns all courses if user is a moderator, otherwise returns only its courses.
    Moderators can't create/delete courses.
    Other methods are allowed only if user is owner or a moderator.

    Created courses linked to request.user automatically.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = MaterialsPaginator

    @override
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="moderators").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    @override
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action == "create":
            permission_classes += [~IsModerator]
        elif self.action == "destroy":
            permission_classes += [~IsModerator, IsOwner]
        elif self.action in ["retrieve", "update", "partial_update", "list"]:
            permission_classes += [IsModerator | IsOwner]

        return [permission() for permission in permission_classes]

    @override
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @override
    def perform_update(self, serializer):
        serializer.save()
        course = serializer.instance

        if (timezone.now() - course.updated_at) > timedelta(hours=4):
            notify_about_course_update.delay(course.id)


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """
    List/Create View for Lesson model.

    Returns all lessons if user is a moderator, otherwise returns only its lessons.
    Created lessons linked to request.user automatically.

    Moderators can't create lessons.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = MaterialsPaginator

    @override
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="moderators").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    @override
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.request.method == "GET":
            permission_classes += [IsModerator | IsOwner]
        elif self.request.method == "POST":
            permission_classes += [~IsModerator]

        return [permission() for permission in permission_classes]

    @override
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve/Update/Destroy View for Lesson model.

    Retrieve/Update methods are allowed only if user is owner or a moderator.
    Moderators can't delete lessons.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    @override
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.request.method in ["GET", "PUT", "PATCH"]:
            permission_classes += [IsModerator | IsOwner]
        elif self.request.method == "DELETE":
            permission_classes += [~IsModerator, IsOwner]

        return [permission() for permission in permission_classes]

    @override
    def perform_update(self, serializer):
        serializer.save()
        course = serializer.instance.course

        if (timezone.now() - course.updated_at) > timedelta(hours=4):
            notify_about_course_update.delay(course.id)
