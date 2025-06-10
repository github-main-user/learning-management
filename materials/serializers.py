from rest_framework.serializers import ModelSerializer

from .models import Course, Lesson


class CourseSerizlizer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerizlizer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
