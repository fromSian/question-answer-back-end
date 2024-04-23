from django.contrib import admin

# Register your models here.
from .models import User

from django.contrib.auth.admin import UserAdmin


class UserProfileAdmin(UserAdmin):
    list_display = [
        "username",
    ]
    ordering = ("-date_joined",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "times",
                    "coins",
                    "groups",
                    "is_superuser",
                    "is_staff",
                    "is_active",
                )
            },
        ),
    )


admin.site.register(User, UserProfileAdmin)
