import uuid
from pathlib import Path

from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import F, Q

from .validators import validate_file_size


class PlacementStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    ACTIVE = "active", "Active"
    COMPLETED = "completed", "Completed"
    REJECTED = "rejected", "Rejected"


# A student may only have one placement in these states (business rule, 4.5).
OPEN_STATUSES = (PlacementStatus.PENDING, PlacementStatus.APPROVED, PlacementStatus.ACTIVE)


class Placement(models.Model):
    placement_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(
        "accounts.Student", on_delete=models.PROTECT, db_column="student_number", related_name="placements"
    )
    organisation = models.ForeignKey(
        "organisations.HostOrganization", on_delete=models.PROTECT, db_column="organisation_id", related_name="placements"
    )
    mentor = models.ForeignKey("accounts.Mentor", on_delete=models.PROTECT, db_column="mentor_id", related_name="placements")
    coordinator = models.ForeignKey(
        "accounts.Coordinator", on_delete=models.PROTECT, db_column="coordinator_id", related_name="placements"
    )
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=PlacementStatus.choices, default=PlacementStatus.PENDING)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "placement"
        ordering = ["-start_date"]
        indexes = [models.Index(fields=["status"], name="placement_status_idx")]
        constraints = [
            models.CheckConstraint(condition=Q(end_date__gt=F("start_date")), name="placement_end_after_start"),
        ]

    def __str__(self):
        return f"Placement {self.pk}: {self.student} at {self.organisation}"

    @property
    def accepts_logbook_entries(self):
        return self.status in (PlacementStatus.APPROVED, PlacementStatus.ACTIVE)


def document_upload_path(instance, filename):
    """Rename uploads to a unique system-generated name (section 4.4.8)."""
    extension = Path(filename).suffix.lower()
    return f"documents/placement_{instance.placement_id}/{uuid.uuid4().hex}{extension}"


class Document(models.Model):
    document_id = models.AutoField(primary_key=True)
    placement = models.ForeignKey(
        Placement, on_delete=models.PROTECT, db_column="placement_id", related_name="documents"
    )
    document_type = models.CharField(max_length=60)
    file_path = models.FileField(
        max_length=500,
        upload_to=document_upload_path,
        validators=[
            FileExtensionValidator(allowed_extensions=settings.DOCUMENT_ALLOWED_EXTENSIONS),
            validate_file_size,
        ],
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "document"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.document_type} for placement {self.placement_id}"

    @property
    def filename(self):
        return Path(self.file_path.name).name
