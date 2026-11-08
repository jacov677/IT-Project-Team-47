from django.contrib import admin
from .models import HostOrganization


@admin.register(HostOrganization)
class HostOrganizationAdmin(admin.ModelAdmin):
    list_display = (
        "organisation_id",
        "organisation_name",
        "registration_number",
        "industry",
        "contact_email",
        "contact_number",
        "is_active",
    )

    list_filter = ("industry", "is_active")

    search_fields = (
        "organisation_name",
        "registration_number",
        "contact_email",
    )

    readonly_fields = ("created_at", "updated_at")
    ordering = ("organisation_name",)
