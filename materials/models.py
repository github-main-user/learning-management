from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    preview = models.ImageField(upload_to="courses/", blank=True, null=True)


class Lesson(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    preview = models.ImageField(upload_to="courses/", blank=True, null=True)
    video_url = models.URLField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
