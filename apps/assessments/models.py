from django.db import models
from apps.accounts.models import Student, Mentor
from apps.placements.models import Placement

class Assessment(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        SUBMITTED = "SUBMITTED", "Submitted"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    placement = models.ForeignKey(Placement, on_delete=models.RESTRICT, related_name="assessments")
    student = models.ForeignKey(Student, on_delete=models.RESTRICT, related_name="assessments")
    mentor = models.ForeignKey(Mentor, on_delete=models.SET_NULL, null=True, blank=True, related_name="assessments")

    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    assessed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "assessment"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.student} - {self.placement} ({self.status})"
