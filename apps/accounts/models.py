"""
Accounts: the shared `user` table and the role profiles linked to it.

Tables (Phase 4, section 4.5): user, student, coordinator, mentor.
Employers are represented through host_organization and mentor records,
as stated in the 4.5 "Model Alignment Considerations".
"""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class Role(models.TextChoices):
    STUDENT = "Student", "Student"
    MENTOR = "Mentor", "Mentor"
    COORDINATOR = "Coordinator", "WIL Coordinator"
    ADMIN = "Admin", "Administrator"


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra):
        if not email:
            raise ValueError("An email address is required.")
        user = self.model(email=self.normalize_email(email).lower(), **extra)
        user.set_password(password)  # stored as a hash, never plain text
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        # Email login is case-insensitive.
        return self.get(email__iexact=username)

    def create_user(self, email, password=None, **extra):
        extra.setdefault("role", Role.STUDENT)
        extra.setdefault("is_staff", False)
        extra.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra)

    def create_superuser(self, email, password=None, **extra):
        extra.update(role=Role.ADMIN, is_staff=True, is_superuser=True, is_active=True)
        return self._create_user(email, password, **extra)


class User(AbstractBaseUser, PermissionsMixin):
    """Authentication account, role, active state and creation timestamp."""

    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=150, unique=True)
    # Django's hashed password field, stored in the `password_hash` column.
    password = models.CharField("password", max_length=255, db_column="password_hash")
    role = models.CharField(max_length=20, choices=Role.choices)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Required by Django's admin site; not part of the logical data dictionary.
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "user"
        ordering = ["email"]

    def __str__(self):
        return self.email

    # Convenience checks used by templates and permission helpers
    @property
    def is_student(self):
        return self.role == Role.STUDENT

    @property
    def is_mentor(self):
        return self.role == Role.MENTOR

    @property
    def is_coordinator(self):
        return self.role == Role.COORDINATOR

    @property
    def is_admin_role(self):
        return self.role == Role.ADMIN

    @property
    def display_name(self):
        profile = self.profile
        if profile is not None:
            return f"{profile.first_name} {profile.last_name}"
        return self.email

    @property
    def profile(self):
        """Return the Student/Mentor/Coordinator profile for this user, if any."""
        attr = {Role.STUDENT: "student", Role.MENTOR: "mentor", Role.COORDINATOR: "coordinator"}.get(self.role)
        return getattr(self, attr, None) if attr else None


class Student(models.Model):
    student_number = models.CharField(max_length=30, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT, db_column="user_id", related_name="student")
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    qualification = models.CharField(max_length=120)
    contact_number = models.CharField(max_length=30, blank=True)

    class Meta:
        db_table = "student"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.student_number} - {self.first_name} {self.last_name}"


class Coordinator(models.Model):
    coordinator_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT, db_column="user_id", related_name="coordinator")
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    department = models.CharField(max_length=120, blank=True)

    class Meta:
        db_table = "coordinator"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Mentor(models.Model):
    mentor_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT, db_column="user_id", related_name="mentor")
    organisation = models.ForeignKey(
        "organisations.HostOrganization", on_delete=models.PROTECT, db_column="organisation_id", related_name="mentors"
    )
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    job_title = models.CharField(max_length=100, blank=True)
    contact_number = models.CharField(max_length=30, blank=True)

    class Meta:
        db_table = "mentor"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.organisation})"
