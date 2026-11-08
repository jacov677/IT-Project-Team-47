from django.contrib import admin
from .models import LogbookEntry

@admin.register(LogbookEntry)
class LogbookEntryAdmin(admin.ModelAdmin):
    list_display = ("student", "placement", "date", "hours_worked", "status")
    list_filter = ("status", "date")
    search_fields = ("student__student_number", "activities")
