from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import AdminUserChangeForm, AdminUserCreationForm
from .models import Coordinator, Mentor, Student, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = AdminUserChangeForm
    add_form = AdminUserCreationForm
    list_display = ("email", "role", "is_active", "is_staff", "created_at")
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("email",)
    ordering = ("email",)
    readonly_fields = ("created_at", "last_login")
    actions = ["activate_users", "deactivate_users"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Role and status", {"fields": ("role", "is_active")}),
        ("Admin site access", {"fields": ("is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Dates", {"fields": ("last_login", "created_at")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "role", "password1", "password2", "is_active")}),
    )

    @admin.action(description="Activate selected accounts")
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} account(s) activated.")

    @admin.action(description="Deactivate selected accounts")
    def deactivate_users(self, request, queryset):
        updated = queryset.exclude(pk=request.user.pk).update(is_active=False)
        self.message_user(request, f"{updated} account(s) deactivated.")


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_number", "first_name", "last_name", "qualification", "user")
    search_fields = ("student_number", "first_name", "last_name", "user__email")
    list_filter = ("qualification",)
    autocomplete_fields = ("user",)


@admin.register(Coordinator)
class CoordinatorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "department", "user")
    search_fields = ("first_name", "last_name", "user__email")
    autocomplete_fields = ("user",)


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "organisation", "job_title", "user")
    search_fields = ("first_name", "last_name", "user__email", "organisation__organisation_name")
    list_filter = ("organisation",)
    autocomplete_fields = ("user", "organisation")
