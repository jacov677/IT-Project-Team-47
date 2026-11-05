
from django.contrib import admin
from .models import Placement, Document


@admin.register(Placement)
class PlacementAdmin(admin.ModelAdmin):
    list_display = ("student_name", "company_name", "position", "status", "start_date")
    list_filter = ("status",)
    search_fields = ("student_name", "company_name")


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("document_name", "document_type", "placement", "uploaded_at")
    list_filter = ("document_type",)
    search_fields = ("document_name",)
