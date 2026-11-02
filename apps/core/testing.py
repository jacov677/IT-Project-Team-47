"""Small helpers that build test records. Import these in any app's tests.

    from apps.core.testing import make_placement
"""
from datetime import timedelta
from itertools import count

from django.utils import timezone

from apps.accounts.models import Coordinator, Mentor, Role, Student, User
from apps.organisations.models import HostOrganization
from apps.placements.models import Placement, PlacementStatus

PASSWORD = "Test-pass-123"
_seq = count(1)


def make_user(role, **extra):
    n = next(_seq)
    return User.objects.create_user(email=f"{role.lower()}{n}@test.local", password=PASSWORD, role=role, **extra)


def make_organisation(**extra):
    n = next(_seq)
    return HostOrganization.objects.create(organisation_name=f"Org {n}", registration_number=f"REG{n}", **extra)


def make_student(**extra):
    n = next(_seq)
    return Student.objects.create(
        student_number=f"S{n:05d}", user=make_user(Role.STUDENT), first_name="Test", last_name=f"Student{n}",
        qualification="BSc IT", **extra
    )


def make_mentor(organisation=None):
    return Mentor.objects.create(
        user=make_user(Role.MENTOR), organisation=organisation or make_organisation(), first_name="Test", last_name="Mentor"
    )


def make_coordinator():
    return Coordinator.objects.create(user=make_user(Role.COORDINATOR), first_name="Test", last_name="Coordinator")


def make_placement(status=PlacementStatus.ACTIVE, student=None, mentor=None, coordinator=None, **extra):
    mentor = mentor or make_mentor()
    today = timezone.localdate()
    defaults = {"start_date": today - timedelta(days=30), "end_date": today + timedelta(days=60)}
    defaults.update(extra)
    return Placement.objects.create(
        student=student or make_student(),
        organisation=mentor.organisation,
        mentor=mentor,
        coordinator=coordinator or make_coordinator(),
        status=status,
        **defaults,
    )
