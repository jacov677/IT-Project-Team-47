
from django.db import models


# Stores daily activities completed by students during placement
class LogbookEntry(models.Model):
    placement = models.ForeignKey(
        "placements.Placement",
        on_delete=models.CASCADE,
        related_name="logbook_entries"
    )
    entry_date = models.DateField()
    activities = models.TextField()
    hours_worked = models.DecimalField(max_digits=4, decimal_places=2)
    supervisor_comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Displays the student and date of the entry
        return f"{self.placement.student_name} - {self.entry_date}"
