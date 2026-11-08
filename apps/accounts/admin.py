from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    User,
    Student,
    Coordinator,
    Mentor,
    EmployerProfile,
)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
        "is_active",
    )

    list_filter = ("role", "is_active", "is_staff")

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "WIL Account Information",
            {
                "fields": (
                    "role",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    readonly_fields = ("created_at", "updated_at")


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "student_number",
        "first_name",
        "last_name",
        "qualification",
        "user",
    )
    search_fields = ("student_number", "first_name", "last_name")


@admin.register(Coordinator)
class CoordinatorAdmin(admin.ModelAdmin):
    list_display = (
        "coordinator_id",
        "first_name",
        "last_name",
        "department",
        "user",
    )
    search_fields = ("first_name", "last_name", "department")


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = (
        "mentor_id",
        "first_name",
        "last_name",
        "organisation",
        "job_title",
        "user",
    )
    list_filter = ("organisation",)
    search_fields = ("first_name", "last_name", "job_title")


@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = (
        "employer_id",
        "first_name",
        "last_name",
        "organisation",
        "job_title",
        "user",
    )
    list_filter = ("organisation",)
    search_fields = ("first_name", "last_name", "job_title")
