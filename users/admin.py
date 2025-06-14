from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "first_name",
        "last_name",
        "avatar",
        "phone",
        "city",
        "is_active",
    ]
    search_fields = ["first_name", "last_name"]
    list_filter = ["city", "is_active"]
