"""
Student Portal models.

Uses the team's shared models instead of its own copies:
  - accounts.Student (Khaya)                    -> the student's core details
  - organisations.PlacementOpportunity (Tshepo) -> the opportunities students apply for
"""
from django.conf import settings
from django.db import models

from apps.accounts.models import Student
from apps.organisations.models import PlacementOpportunity


class StudentPortalProfile(models.Model):
    """Extra portal details for a student (skills, bio, CV).

    Name, student number, programme (qualification) and phone (contact_number)
    stay on accounts.Student so there is only one copy of them.
    """

    class Year(models.IntegerChoices):
        FIRST = 1, "1st year"
        SECOND = 2, "2nd year"
        THIRD = 3, "3rd year"
        FOURTH = 4, "4th year"

    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name="portal_profile")
    year_of_study = models.PositiveSmallIntegerField(choices=Year.choices, default=Year.THIRD)
    skills = models.TextField(blank=True, help_text="Comma-separated, e.g. Python, SQL, Figma")
    bio = models.TextField(blank=True)
    cv = models.FileField(upload_to="cvs/", blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "student_portal_profile"

    def __str__(self):
        return f"Portal profile - {self.student}"

    # Shortcuts so the templates can read the student's core details from one place.
    @property
    def student_number(self):
        return self.student.student_number

    @property
    def programme(self):
        return self.student.qualification

    @property
    def phone(self):
        return self.student.contact_number

    @property
    def completeness(self):
        """Percentage of optional profile fields that are filled in."""
        fields = [self.phone, self.programme, self.skills, self.bio, self.cv]
        return int(sum(1 for f in fields if f) / len(fields) * 100)

    @property
    def skills_list(self):
        return [s.strip() for s in self.skills.split(",") if s.strip()]


class Application(models.Model):
    """A student's application for a placement opportunity."""

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        UNDER_REVIEW = "UNDER_REVIEW", "Under review"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"
        WITHDRAWN = "WITHDRAWN", "Withdrawn"

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="applications")
    opportunity = models.ForeignKey(PlacementOpportunity, on_delete=models.CASCADE, related_name="applications")
    cover_letter = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    date_applied = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "application"
        ordering = ["-date_applied"]
        constraints = [
            models.UniqueConstraint(fields=["student", "opportunity"], name="one_application_per_opportunity")
        ]

    def __str__(self):
        return f"{self.student} -> {self.opportunity}"

    @property
    def can_withdraw(self):
        return self.status in (self.Status.PENDING, self.Status.UNDER_REVIEW)


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=120)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notification"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.title}"
