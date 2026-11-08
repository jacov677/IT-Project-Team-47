from django.db import models
from apps.accounts.models import Student, Coordinator
from apps.placements.models import Placement

class Report(models.Model):
    class ReportType(models.TextChoices):
        PLACEMENT = "PLACEMENT", "Placement Report"
        LOGBOOK = "LOGBOOK", "Logbook Report"
        ASSESSMENT = "ASSESSMENT", "Assessment Report"
        OTHER = "OTHER", "Other"

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        SUBMITTED = "SUBMITTED", "Submitted"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    placement = models.ForeignKey(Placement, on_delete=models.RESTRICT, related_name="reports")
    student = models.ForeignKey(Student, on_delete=models.RESTRICT, related_name="reports")
    coordinator = models.ForeignKey(Coordinator, on_delete=models.SET_NULL, null=True, blank=True, related_name="reports")

    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=ReportType.choices, default=ReportType.PLACEMENT)
    summary = models.TextField(blank=True)
    file_path = models.FileField(upload_to="reports/", null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    approved_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "report"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.student} ({self.status})"
