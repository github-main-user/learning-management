from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from .models import Course


@shared_task
def notify_about_course_update(course_id: int) -> None:
    """Sends email to all subscribed to given course users."""

    course = Course.objects.get(id=course_id)
    if not course.subscriptions.exists():
        print(f"Given course ({course}) doesn't have any subscriptions")
        return

    send_mail(
        "One of courses you are subscribed got an update",
        f"Hi! Course {course.title} was updated!",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[sub.user.email for sub in course.subscriptions],
        fail_silently=False,
    )
