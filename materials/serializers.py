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
    is_subscribed = serializers.SerializerMethodField()

    def get_lessons_count(self, instance):
        return instance.lessons.count()

    def get_is_subscribed(self, instance):
        user = self.context["request"].user
        if user.is_authenticated:
            return user.subscriptions.filter(course=instance).exists()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "preview",
            "lessons",
            "lessons_count",
            "is_subscribed",
        ]
