from django.contrib import admin

from .models import Application, Notification, StudentPortalProfile


@admin.register(StudentPortalProfile)
class StudentPortalProfileAdmin(admin.ModelAdmin):
    list_display = ("student", "year_of_study", "updated_at")
    search_fields = ("student__student_number", "student__first_name", "student__last_name")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("student", "opportunity", "status", "date_applied")
    list_filter = ("status",)
    search_fields = ("student__student_number", "student__last_name", "opportunity__title")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "is_read", "created_at")
    list_filter = ("is_read",)
