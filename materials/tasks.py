from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone

from .models import Course

User = get_user_model()


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


@shared_task
def block_inactive_users() -> None:
    """Blocks users that weren't active last 30 days."""

    month_ago = timezone.now() - timedelta(days=30)
    selected_users = User.objects.filter(
        last_login__lt=month_ago, is_active=True, is_staff=False, is_superuser=False
    )
    selected_users.update(is_active=False)
