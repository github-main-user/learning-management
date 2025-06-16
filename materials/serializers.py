from rest_framework import serializers

from .models import Course, Lesson
from .validators import AllowedURLValidator


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[AllowedURLValidator()])

    class Meta:
        model = Lesson
        fields = ["id", "title", "description", "preview", "video_url", "course"]


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField()

    def get_lessons_count(self, instance):
        return instance.lessons.count()

    class Meta:
        model = Course
        fields = ["id", "title", "description", "preview", "lessons", "lessons_count"]
