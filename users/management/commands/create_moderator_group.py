from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from materials.models import Course, Lesson


class Command(BaseCommand):
    help = "Creates the 'Moderator' group with specific permissions"

    def handle(self, *args, **options):
        group_name = "moderators"
        permissions_needed = [
            ("view_lesson", Lesson),
            ("change_lesson", Lesson),
            ("view_course", Course),
            ("change_course", Course),
        ]

        group, _ = Group.objects.get_or_create(name=group_name)

        for codename, model in permissions_needed:
            content_type = ContentType.objects.get_for_model(model)
            try:
                permission = Permission.objects.get(
                    codename=codename, content_type=content_type
                )
                group.permissions.add(permission)
                self.stdout.write(self.style.SUCCESS(f"Added {codename} permission."))
            except Permission.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Permission {codename} not found."))

        self.stdout.write(self.style.SUCCESS(f"Group '{group_name}' is ready."))
