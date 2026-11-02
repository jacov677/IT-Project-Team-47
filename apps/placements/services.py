"""Placement business rules (sections 4.1 and 4.5).

Every multi-step action runs inside transaction.atomic() so related updates
succeed or roll back together.
"""
from django.db import transaction
from django.utils import timezone

from apps.audit.services import log_action
from apps.core.exceptions import BusinessRuleError, NotAllowed
from apps.core.notifications import send_notification

from .models import OPEN_STATUSES, Placement, PlacementStatus


def student_has_open_placement(student, exclude=None):
    qs = Placement.objects.filter(student=student, status__in=OPEN_STATUSES)
    if exclude is not None:
        qs = qs.exclude(pk=exclude.pk)
    return qs.exists()


@transaction.atomic
def create_placement(*, user, student, organisation, mentor, coordinator, start_date, end_date):
    """Create a pending placement. A student may only have one open placement."""
    if mentor.organisation_id != organisation.pk:
        raise BusinessRuleError("The mentor does not belong to the selected host organisation.")
    if end_date <= start_date:
        raise BusinessRuleError("The end date must be after the start date.")
    # Lock the student's placements so two requests cannot both pass the check.
    list(Placement.objects.select_for_update().filter(student=student))
    if student_has_open_placement(student):
        raise BusinessRuleError("This student already has an open placement.")

    placement = Placement.objects.create(
        student=student,
        organisation=organisation,
        mentor=mentor,
        coordinator=coordinator,
        start_date=start_date,
        end_date=end_date,
        status=PlacementStatus.PENDING,
    )
    log_action(user, "Create placement", placement)
    send_notification(coordinator.user, "New placement awaiting approval",
                      f"A placement for {student} at {organisation} is waiting for your approval.")
    return placement


@transaction.atomic
def approve_placement(placement, coordinator_user):
    if not coordinator_user.is_coordinator:
        raise NotAllowed("Only a WIL coordinator can approve placements.")
    placement = Placement.objects.select_for_update().get(pk=placement.pk)
    if placement.status != PlacementStatus.PENDING:
        raise BusinessRuleError("This placement is not waiting for approval.")
    if Placement.objects.filter(
        student=placement.student, status__in=(PlacementStatus.APPROVED, PlacementStatus.ACTIVE)
    ).exclude(pk=placement.pk).exists():
        raise BusinessRuleError("This student already has an approved placement.")

    placement.status = PlacementStatus.APPROVED
    placement.approved_at = timezone.now()
    placement.coordinator = coordinator_user.coordinator
    placement.save(update_fields=["status", "approved_at", "coordinator"])
    log_action(coordinator_user, "Approve placement", placement)

    def notify():
        send_notification(placement.student.user, "Placement approved",
                          f"Your WIL placement at {placement.organisation} has been approved.")
        send_notification(placement.mentor.user, "New student assigned",
                          f"You are now the mentor for {placement.student}.")

    transaction.on_commit(notify)
    return placement


@transaction.atomic
def reject_placement(placement, coordinator_user, reason=""):
    if not coordinator_user.is_coordinator:
        raise NotAllowed("Only a WIL coordinator can reject placements.")
    placement = Placement.objects.select_for_update().get(pk=placement.pk)
    if placement.status != PlacementStatus.PENDING:
        raise BusinessRuleError("This placement is not waiting for approval.")
    placement.status = PlacementStatus.REJECTED
    placement.save(update_fields=["status"])
    log_action(coordinator_user, "Reject placement", placement)
    transaction.on_commit(lambda: send_notification(
        placement.student.user, "Placement not approved",
        f"Your placement request at {placement.organisation} was not approved. {reason}".strip()))
    return placement


def activate_due_placements():
    """Move approved placements to active once their start date arrives.

    Run daily, e.g. `python manage.py activate_placements` from cron.
    """
    return Placement.objects.filter(
        status=PlacementStatus.APPROVED, start_date__lte=timezone.localdate()
    ).update(status=PlacementStatus.ACTIVE)


def user_can_view_placement(user, placement):
    if user.is_coordinator or user.is_admin_role:
        return True
    if user.is_student:
        return placement.student.user_id == user.pk
    if user.is_mentor:
        return placement.mentor.user_id == user.pk
    return False
