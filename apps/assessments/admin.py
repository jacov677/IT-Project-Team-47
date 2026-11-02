from django.contrib import admin

from .models import AssessmentResult, Evaluation


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ("evaluation_id", "placement", "rating", "submitted_at")
    list_filter = ("rating",)


@admin.register(AssessmentResult)
class AssessmentResultAdmin(admin.ModelAdmin):
    list_display = ("result_id", "placement", "final_mark", "coordinator", "captured_at")
