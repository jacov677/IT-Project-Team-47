from django.contrib import admin

from .models import Document, Placement


class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0
    readonly_fields = ("uploaded_at",)


@admin.register(Placement)
class PlacementAdmin(admin.ModelAdmin):
    list_display = ("placement_id", "student", "organisation", "mentor", "status", "start_date", "end_date")
    list_filter = ("status", "organisation")
    search_fields = ("student__student_number", "student__last_name", "organisation__organisation_name")
    autocomplete_fields = ("student", "organisation", "mentor", "coordinator")
    readonly_fields = ("approved_at",)
    date_hierarchy = "start_date"
    inlines = [DocumentInline]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("document_id", "document_type", "placement", "uploaded_at")
    list_filter = ("document_type",)
    readonly_fields = ("uploaded_at",)
