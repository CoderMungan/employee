from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_manager",
        "is_employee",
        "user_type",
    )
    list_filter = ("is_staff", "is_active")
    ordering = ("email",)
    search_fields = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal Info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "remaining_leave_days",
                    "used_leave_days",
                    "total_late_minutes",
                    "monthly_working_hours",
                    "user_type",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_manager",
                    "is_employee",
                )
            },
        ),
        ("Related Models", {"fields": ("leaverequest", "worklog")}),  # Burada ekliyoruz
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_manager",
                    "is_employee",
                    "leaverequest",
                    "worklog",
                ),
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
