from django.contrib import admin
from .models import Placement, Document

@admin.register(Placement)
class PlacementAdmin(admin.ModelAdmin):
    list_display = ("student", "organisation", "mentor", "status", "start_date", "end_date")
    list_filter = ("status",)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "placement", "doc_type", "uploaded_at")
    list_filter = ("doc_type",)
