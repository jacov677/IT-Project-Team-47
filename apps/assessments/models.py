from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone

# Rating scale for the mentor evaluation. Section 4.5 leaves the range to the
# group; 1-5 is used here. Change both values and make a migration if needed.
RATING_MIN, RATING_MAX = 1, 5


class Evaluation(models.Model):
    """Mentor's final evaluation. At most one per placement."""

    evaluation_id = models.AutoField(primary_key=True)
    placement = models.OneToOneField(
        "placements.Placement", on_delete=models.PROTECT, db_column="placement_id", related_name="evaluation"
    )
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(RATING_MIN), MaxValueValidator(RATING_MAX)])
    comments = models.TextField(blank=True)
    submitted_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "evaluation"
        constraints = [
            models.CheckConstraint(
                condition=Q(rating__gte=RATING_MIN) & Q(rating__lte=RATING_MAX), name="evaluation_rating_in_range"
            ),
        ]

    def __str__(self):
        return f"Evaluation for placement {self.placement_id}: {self.rating}/{RATING_MAX}"


class AssessmentResult(models.Model):
    """Final WIL mark captured by a coordinator. At most one per placement."""

    result_id = models.AutoField(primary_key=True)
    placement = models.OneToOneField(
        "placements.Placement", on_delete=models.PROTECT, db_column="placement_id", related_name="assessment_result"
    )
    coordinator = models.ForeignKey(
        "accounts.Coordinator", on_delete=models.PROTECT, db_column="coordinator_id", related_name="captured_results"
    )
    final_mark = models.DecimalField(
        max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    captured_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "assessment_result"
        constraints = [
            models.CheckConstraint(
                condition=Q(final_mark__gte=0) & Q(final_mark__lte=100), name="final_mark_between_0_and_100"
            ),
        ]

    def __str__(self):
        return f"Result for placement {self.placement_id}: {self.final_mark}%"
