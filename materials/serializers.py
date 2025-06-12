from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "title", "description", "preview", "video_url", "course"]


class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = SerializerMethodField()

    def get_lessons_count(self, instance):
        return instance.lessons.count()

    class Meta:
        model = Course
        fields = ["id", "title", "description", "preview", "lessons", "lessons_count"]
