# Generated by Django 5.2.3 on 2025-06-10 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="course",
            old_name="name",
            new_name="title",
        ),
        migrations.RemoveField(
            model_name="lesson",
            name="name",
        ),
        migrations.AddField(
            model_name="lesson",
            name="title",
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
