"""Evaluation and final result business rules (sections 4.1 and 4.5)."""
from django.db import transaction
from django.utils import timezone

from apps.audit.services import log_action
from apps.core.exceptions import BusinessRuleError, NotAllowed
from apps.core.notifications import send_notification
from apps.placements.models import Placement, PlacementStatus

from .models import RATING_MAX, RATING_MIN, AssessmentResult, Evaluation


@transaction.atomic
def submit_evaluation(mentor_user, placement, *, rating, comments=""):
    if not mentor_user.is_mentor or placement.mentor.user_id != mentor_user.pk:
        raise NotAllowed("Only the mentor assigned to this placement can submit its evaluation.")
    if Evaluation.objects.filter(placement=placement).exists():
        raise BusinessRuleError("An evaluation has already been submitted for this placement.")
    if not (RATING_MIN <= rating <= RATING_MAX):
        raise BusinessRuleError(f"The rating must be between {RATING_MIN} and {RATING_MAX}.")
    evaluation = Evaluation.objects.create(placement=placement, rating=rating, comments=comments)
    log_action(mentor_user, "Submit evaluation", evaluation)
    transaction.on_commit(lambda: send_notification(
        placement.coordinator.user, "Mentor evaluation submitted",
        f"The mentor evaluation for {placement.student} has been submitted."))
    return evaluation


def result_blockers(placement):
    """Return a list of reasons a final result cannot be captured yet (empty list = ready)."""
    reasons = []
    entries = placement.logbook_entries.all()
    if not entries.exists():
        reasons.append("No logbook entries have been submitted.")
    else:
        unsigned = entries.filter(mentor_signed_off=False).count()
        if unsigned:
            reasons.append(f"{unsigned} logbook entr{'y is' if unsigned == 1 else 'ies are'} not signed off.")
    if not Evaluation.objects.filter(placement=placement).exists():
        reasons.append("The mentor has not submitted the evaluation.")
    if AssessmentResult.objects.filter(placement=placement).exists():
        reasons.append("A final result has already been captured.")
    return reasons


@transaction.atomic
def capture_final_result(coordinator_user, placement, final_mark):
    if not coordinator_user.is_coordinator:
        raise NotAllowed("Only a WIL coordinator can capture final results.")
    placement = Placement.objects.select_for_update().get(pk=placement.pk)
    blockers = result_blockers(placement)
    if blockers:
        raise BusinessRuleError(" ".join(blockers))
    if not (0 <= final_mark <= 100):
        raise BusinessRuleError("The final mark must be between 0 and 100.")

    result = AssessmentResult.objects.create(
        placement=placement, coordinator=coordinator_user.coordinator, final_mark=final_mark, captured_at=timezone.now()
    )
    placement.status = PlacementStatus.COMPLETED
    placement.save(update_fields=["status"])
    log_action(coordinator_user, "Capture final result", result)
    transaction.on_commit(lambda: send_notification(
        placement.student.user, "WIL result available", "Your final WIL result has been captured."))
    return result
