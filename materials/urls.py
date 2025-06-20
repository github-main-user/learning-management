from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.views import CourseViewAPISet

from .apps import MaterialsConfig
from .views import (
    CourseSubscriptionAPIView,
    LessonListCreateAPIView,
    LessonRetrieveUpdateDestroyAPIView,
)

app_name = MaterialsConfig.name

courses_router = DefaultRouter()
courses_router.register(r"courses", CourseViewAPISet, basename="course")

urlpatterns = [
    *courses_router.urls,
    path(
        "courses/<int:pk>/subscription/",
        CourseSubscriptionAPIView.as_view(),
        name="course-subscription",
    ),
    path("lessons/", LessonListCreateAPIView.as_view(), name="lesson-list"),
    path(
        "lessons/<int:pk>/",
        LessonRetrieveUpdateDestroyAPIView.as_view(),
        name="lesson-detail",
    ),
]
