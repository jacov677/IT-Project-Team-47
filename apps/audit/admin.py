from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """Read-only: audit records must never be edited or deleted."""

    list_display = ("logged_at", "user", "action", "table_name", "record_id")
    list_filter = ("table_name",)
    search_fields = ("user__email", "action", "record_id")
    date_hierarchy = "logged_at"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
