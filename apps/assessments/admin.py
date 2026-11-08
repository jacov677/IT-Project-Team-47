from django.contrib import admin
from .models import Assessment

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ("student", "placement", "mentor", "score", "status", "assessed_at")
    list_filter = ("status",)
