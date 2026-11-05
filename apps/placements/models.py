from django.db import models
from apps.accounts.models import Student, Coordinator, Mentor
from apps.organisations.models import HostOrganization

class Placement(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"
        ACTIVE = "ACTIVE", "Active"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    student = models.ForeignKey(Student, on_delete=models.RESTRICT, related_name="placements")
    organisation = models.ForeignKey(HostOrganization, on_delete=models.RESTRICT, related_name="placements")
    mentor = models.ForeignKey(Mentor, on_delete=models.SET_NULL, null=True, blank=True, related_name="placements")
    coordinator = models.ForeignKey(Coordinator, on_delete=models.SET_NULL, null=True, blank=True, related_name="placements")

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    approved_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "placement"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.student} - {self.organisation} ({self.status})"

class Document(models.Model):
    class DocType(models.TextChoices):
        CV = "CV", "CV"
        CONTRACT = "CONTRACT", "Contract"
        LOGBOOK = "LOGBOOK", "Logbook"
        REPORT = "REPORT", "Report"
        OTHER = "OTHER", "Other"

    placement = models.ForeignKey(Placement, on_delete=models.CASCADE, related_name="documents")
    title = models.CharField(max_length=200)
    document_type = models.CharField(max_length=20, choices=DocType.choices, default=DocType.OTHER)
    file_path = models.FileField(upload_to="placement_documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "document"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.title} - {self.placement}"
