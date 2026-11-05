
from django.contrib import admin
from .models import LogbookEntry


# Register student logbook entries in the admin panel
@admin.register(LogbookEntry)
class LogbookEntryAdmin(admin.ModelAdmin):
    list_display = ("placement", "entry_date", "hours_worked")
    list_filter = ("entry_date",)
    search_fields = ("activities",)
