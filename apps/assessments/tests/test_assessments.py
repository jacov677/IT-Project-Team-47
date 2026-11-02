from datetime import timedelta
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from apps.assessments.services import capture_final_result, submit_evaluation
from apps.core.exceptions import BusinessRuleError, NotAllowed
from apps.core.testing import make_mentor, make_placement
from apps.logbook.services import sign_off_entry, submit_entry
from apps.placements.models import PlacementStatus


class AssessmentRuleTests(TestCase):
    def setUp(self):
        self.placement = make_placement(status=PlacementStatus.ACTIVE)
        self.mentor_user = self.placement.mentor.user
        self.coordinator_user = self.placement.coordinator.user
        self.entry = submit_entry(self.placement.student.user, self.placement,
                                  entry_date=timezone.localdate() - timedelta(days=1),
                                  hours_worked=Decimal("8"), description="Work done")

    def test_only_assigned_mentor_can_evaluate(self):
        with self.assertRaises(NotAllowed):
            submit_evaluation(make_mentor().user, self.placement, rating=4)

    def test_one_evaluation_per_placement(self):
        submit_evaluation(self.mentor_user, self.placement, rating=4)
        with self.assertRaises(BusinessRuleError):
            submit_evaluation(self.mentor_user, self.placement, rating=5)

    def test_result_blocked_until_logbook_signed_off_and_evaluated(self):
        with self.assertRaises(BusinessRuleError):
            capture_final_result(self.coordinator_user, self.placement, Decimal("70"))
        sign_off_entry(self.mentor_user, self.entry)
        with self.assertRaises(BusinessRuleError):  # still no evaluation
            capture_final_result(self.coordinator_user, self.placement, Decimal("70"))

    def test_capture_result_completes_placement(self):
        sign_off_entry(self.mentor_user, self.entry)
        submit_evaluation(self.mentor_user, self.placement, rating=4)
        result = capture_final_result(self.coordinator_user, self.placement, Decimal("72.5"))
        self.placement.refresh_from_db()
        self.assertEqual(result.final_mark, Decimal("72.5"))
        self.assertEqual(self.placement.status, PlacementStatus.COMPLETED)

    def test_mark_must_be_0_to_100(self):
        sign_off_entry(self.mentor_user, self.entry)
        submit_evaluation(self.mentor_user, self.placement, rating=4)
        with self.assertRaises(BusinessRuleError):
            capture_final_result(self.coordinator_user, self.placement, Decimal("101"))
