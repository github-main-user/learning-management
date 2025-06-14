from typing import override

from rest_framework import generics, viewsets

from users.permissions import IsModerator, IsOwner

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


class CourseViewAPISet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @override
    def get_permissions(self):
        permission_classes = []
        if self.action in ["create", "destroy"]:
            permission_classes = [~IsModerator, IsOwner]
        elif self.action == "list":
            permission_classes = [IsModerator]
        elif self.action in ["retrieve", "update", "partial_update"]:
            permission_classes = [IsModerator | IsOwner]

        return [permission() for permission in permission_classes]

    @override
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    @override
    def get_permissions(self):
        permission_classes = []
        if self.request.method == "GET":
            permission_classes = [IsModerator]
        elif self.request.method == "POST":
            permission_classes = [~IsModerator, IsOwner]

        return [permission() for permission in permission_classes]

    @override
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
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
