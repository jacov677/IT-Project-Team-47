from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("title", "student", "placement", "report_type", "status")
    list_filter = ("status", "report_type")
