from django.contrib import admin

from .models import HostOrganization


@admin.register(HostOrganization)
class HostOrganizationAdmin(admin.ModelAdmin):
    list_display = ("organisation_name", "registration_number", "industry", "contact_email")
    search_fields = ("organisation_name", "registration_number")
    list_filter = ("industry",)
