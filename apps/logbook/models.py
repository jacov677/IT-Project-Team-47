from django.db import models
from apps.accounts.models import Student
from apps.placements.models import Placement

class LogbookEntry(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        SUBMITTED = "SUBMITTED", "Submitted"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    placement = models.ForeignKey(Placement, on_delete=models.CASCADE, related_name="logbook_entries")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="logbook_entries")

    date = models.DateField()
    hours_worked = models.DecimalField(max_digits=4, decimal_places=2)
    activities = models.TextField()
    skills_learned = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    mentor_feedback = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "logbook_entry"
        ordering = ["-date"]

    def __str__(self):
        return f"{self.student} - {self.date} ({self.status})"
