from typing import override

from rest_framework import generics, viewsets

from users.permissions import IsModerator, IsOwner

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


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

    @override
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="moderators").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    @override
    def get_permissions(self):
        permission_classes = []
        if self.action in ["create", "destroy"]:
            permission_classes = [~IsModerator, IsOwner]
        elif self.action in ["retrieve", "update", "partial_update", "list"]:
            permission_classes = [IsModerator | IsOwner]

        return [permission() for permission in permission_classes]

    @override
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """
    List/Create View for Lesson model.

    Returns all lessons if user is a moderator, otherwise returns only its lessons.
    Created lessons linked to request.user automatically.

    Moderators can't create lessons.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    @override
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="moderators").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    @override
    def get_permissions(self):
        permission_classes = []
        if self.request.method == "GET":
            permission_classes = [IsModerator | IsOwner]
        elif self.request.method == "POST":
            permission_classes = [~IsModerator, IsOwner]

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
        permission_classes = []
        if self.request.method == ["GET", "PUT", "PATCH"]:
            permission_classes = [IsModerator | IsOwner]
        elif self.request.method == "DELETE":
            permission_classes = [~IsModerator, IsOwner]

        return [permission() for permission in permission_classes]
