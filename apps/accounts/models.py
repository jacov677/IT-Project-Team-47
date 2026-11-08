
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        COORDINATOR = "COORDINATOR", "Coordinator"
        MENTOR = "MENTOR", "Mentor"
        EMPLOYER = "EMPLOYER", "Employer"
        ADMIN = "ADMIN", "Administrator"

    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
        db_index=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Student(models.Model):
    student_number = models.CharField(
        max_length=30,
        primary_key=True,
    )

    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        related_name="student_profile",
    )

    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    qualification = models.CharField(max_length=120)
    contact_number = models.CharField(max_length=30, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.student_number} - "
            f"{self.first_name} {self.last_name}"
        )


class Coordinator(models.Model):
    coordinator_id = models.AutoField(primary_key=True)

    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        related_name="coordinator_profile",
    )

    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    department = models.CharField(max_length=120)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.coordinator_id} - "
            f"{self.first_name} {self.last_name}"
        )


class Mentor(models.Model):
    mentor_id = models.AutoField(primary_key=True)

    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        related_name="mentor_profile",
    )

    organisation = models.ForeignKey(
        "organisations.HostOrganization",
        on_delete=models.PROTECT,
        related_name="mentors",
    )

    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    job_title = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=30, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.mentor_id} - "
            f"{self.first_name} {self.last_name}"
        )


class EmployerProfile(models.Model):
    """
    Gives an organization representative their own login account.

    An organization can have multiple employer representatives.
    Each representative has one user account.
    """

    employer_id = models.AutoField(primary_key=True)

    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        related_name="employer_profile",
    )

    organisation = models.ForeignKey(
        "organisations.HostOrganization",
        on_delete=models.PROTECT,
        related_name="employer_representatives",
    )

    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    job_title = models.CharField(max_length=100, blank=True)
    contact_number = models.CharField(max_length=30, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.first_name} {self.last_name} - "
            f"{self.organisation}"
        )

class AuditLog(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=50) # e.g. CREATE, UPDATE, DELETE, LOGIN
    table_name = models.CharField(max_length=50) # e.g. Placement, LogbookEntry
    record_id = models.IntegerField(null=True, blank=True)
    details = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "audit_log"
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.user} - {self.action} on {self.table_name} #{self.record_id}"
