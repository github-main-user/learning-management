from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.views import CourseViewSet

from .apps import MaterialsConfig
from .views import LessonListCreateView, LessonRetrieveUpdateDestroyView

app_name = MaterialsConfig.name

courses_router = DefaultRouter()
courses_router.register(r"courses", CourseViewSet, basename="course")

urlpatterns = [
    *courses_router.urls,
    path("lessons/", LessonListCreateView.as_view(), name="lessons-list-create"),
    path(
        "lessons/<int:pk>/",
        LessonRetrieveUpdateDestroyView.as_view(),
        name="lesson-detail",
    ),
]
