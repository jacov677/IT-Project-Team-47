from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q


class LogbookEntry(models.Model):
    entry_id = models.AutoField(primary_key=True)
    placement = models.ForeignKey(
        "placements.Placement", on_delete=models.PROTECT, db_column="placement_id", related_name="logbook_entries"
    )
    entry_date = models.DateField()
    hours_worked = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.25")), MaxValueValidator(Decimal("24"))],
    )
    description = models.TextField()
    mentor_signed_off = models.BooleanField(default=False)
    signed_off_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "logbook_entry"
        ordering = ["-entry_date"]
        verbose_name_plural = "logbook entries"
        constraints = [
            models.CheckConstraint(
                condition=Q(hours_worked__gt=0) & Q(hours_worked__lte=24), name="logbook_hours_between_0_and_24"
            ),
        ]

    def __str__(self):
        return f"{self.entry_date} ({self.hours_worked} h) - placement {self.placement_id}"
