from django.contrib import admin

from .models import LogbookEntry


@admin.register(LogbookEntry)
class LogbookEntryAdmin(admin.ModelAdmin):
    list_display = ("entry_id", "placement", "entry_date", "hours_worked", "mentor_signed_off")
    list_filter = ("mentor_signed_off",)
    search_fields = ("placement__student__student_number", "description")
    date_hierarchy = "entry_date"
    readonly_fields = ("signed_off_at",)
