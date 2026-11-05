
from django.db import models


class Placement(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Completed", "Completed"),
    ]

    student_name = models.CharField(max_length=150)
    company_name = models.CharField(max_length=150)
    position = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.company_name}"


class Document(models.Model):
    DOCUMENT_TYPES = [
        ("CV", "CV"),
        ("Agreement", "Placement Agreement"),
        ("Proof", "Proof of Placement"),
        ("Other", "Other"),
    ]

    placement = models.ForeignKey(
        Placement,
        on_delete=models.CASCADE,
        related_name="documents"
    )
    document_name = models.CharField(max_length=150)
    file = models.FileField(upload_to="documents/")
    document_type = models.CharField(
        max_length=20,
        choices=DOCUMENT_TYPES,
        default="Other"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.document_name
