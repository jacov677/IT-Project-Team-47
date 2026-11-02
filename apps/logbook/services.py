"""Logbook business rules (sections 4.1 and 4.5)."""
from django.db import transaction
from django.utils import timezone

from apps.audit.services import log_action
from apps.core.exceptions import BusinessRuleError, NotAllowed
from apps.core.notifications import send_notification

from .models import LogbookEntry


def _require_own_placement(student_user, placement):
    if not student_user.is_student or placement.student.user_id != student_user.pk:
        raise NotAllowed("You can only add logbook entries to your own placement.")


def _require_assigned_mentor(mentor_user, placement):
    if not mentor_user.is_mentor or placement.mentor.user_id != mentor_user.pk:
        raise NotAllowed("Only the mentor assigned to this placement can do this.")


def _validate_entry(placement, entry_date, hours_worked):
    if not placement.accepts_logbook_entries:
        raise BusinessRuleError("Logbook entries can only be added once the placement is approved.")
    if entry_date > timezone.localdate():
        raise BusinessRuleError("The entry date cannot be in the future.")
    if not (placement.start_date <= entry_date <= placement.end_date):
        raise BusinessRuleError("The entry date must fall inside the placement period.")
    if not (0 < hours_worked <= 24):
        raise BusinessRuleError("Hours worked must be more than 0 and not more than 24.")


@transaction.atomic
def submit_entry(student_user, placement, *, entry_date, hours_worked, description):
    _require_own_placement(student_user, placement)
    _validate_entry(placement, entry_date, hours_worked)
    if not description.strip():
        raise BusinessRuleError("Please describe the work you did.")
    entry = LogbookEntry.objects.create(
        placement=placement, entry_date=entry_date, hours_worked=hours_worked, description=description
    )
    log_action(student_user, "Submit logbook entry", entry)
    transaction.on_commit(lambda: send_notification(
        placement.mentor.user, "Logbook entry submitted",
        f"{placement.student} submitted a logbook entry for {entry_date}."))
    return entry


@transaction.atomic
def edit_entry(student_user, entry, *, hours_worked, description):
    entry = LogbookEntry.objects.select_for_update().get(pk=entry.pk)
    _require_own_placement(student_user, entry.placement)
    if entry.mentor_signed_off:
        raise BusinessRuleError("This entry has been signed off and can no longer be changed.")
    _validate_entry(entry.placement, entry.entry_date, hours_worked)
    entry.hours_worked = hours_worked
    entry.description = description
    entry.save(update_fields=["hours_worked", "description"])
    log_action(student_user, "Edit logbook entry", entry)
    return entry


@transaction.atomic
def sign_off_entry(mentor_user, entry):
    entry = LogbookEntry.objects.select_for_update().get(pk=entry.pk)
    _require_assigned_mentor(mentor_user, entry.placement)
    if entry.mentor_signed_off:
        raise BusinessRuleError("This entry is already signed off.")
    entry.mentor_signed_off = True
    entry.signed_off_at = timezone.now()
    entry.save(update_fields=["mentor_signed_off", "signed_off_at"])
    log_action(mentor_user, "Sign off logbook entry", entry)
    return entry


@transaction.atomic
def reopen_entry(mentor_user, entry, reason):
    """Only the assigned mentor may reopen a signed-off entry; the action is audited."""
    entry = LogbookEntry.objects.select_for_update().get(pk=entry.pk)
    _require_assigned_mentor(mentor_user, entry.placement)
    if not entry.mentor_signed_off:
        raise BusinessRuleError("This entry is not signed off.")
    if not reason.strip():
        raise BusinessRuleError("Please give a reason for reopening the entry.")
    entry.mentor_signed_off = False
    entry.signed_off_at = None
    entry.save(update_fields=["mentor_signed_off", "signed_off_at"])
    log_action(mentor_user, f"Reopen logbook entry: {reason}", entry)
    transaction.on_commit(lambda: send_notification(
        entry.placement.student.user, "Logbook entry reopened",
        f"Your mentor reopened your entry for {entry.entry_date}: {reason}"))
    return entry
