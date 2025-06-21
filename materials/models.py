from django.conf import settings
from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    preview = models.ImageField(upload_to="courses/previews/", blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="courses"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    preview = models.ImageField(upload_to="lessons/previews/", blank=True, null=True)
    video_url = models.URLField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lessons"
    )

    def __str__(self) -> str:
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="subscriptions"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "course"], name="unique_course_per_user"
            )
        ]

    def __str__(self) -> str:
        return f"Subscription: {self.user} - {self.course}"
