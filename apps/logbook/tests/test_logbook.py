from datetime import timedelta
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from apps.audit.models import AuditLog
from apps.core.exceptions import BusinessRuleError, NotAllowed
from apps.core.testing import make_mentor, make_placement
from apps.logbook.services import edit_entry, reopen_entry, sign_off_entry, submit_entry
from apps.placements.models import PlacementStatus


class LogbookRuleTests(TestCase):
    def setUp(self):
        self.placement = make_placement(status=PlacementStatus.ACTIVE)
        self.student_user = self.placement.student.user
        self.mentor_user = self.placement.mentor.user
        self.yesterday = timezone.localdate() - timedelta(days=1)

    def _submit(self, **overrides):
        data = dict(entry_date=self.yesterday, hours_worked=Decimal("8"), description="Configured servers.")
        data.update(overrides)
        return submit_entry(self.student_user, self.placement, **data)

    def test_student_submits_entry(self):
        entry = self._submit()
        self.assertFalse(entry.mentor_signed_off)

    def test_no_entries_before_placement_is_approved(self):
        pending = make_placement(status=PlacementStatus.PENDING)
        with self.assertRaises(BusinessRuleError):
            submit_entry(pending.student.user, pending, entry_date=self.yesterday,
                         hours_worked=Decimal("8"), description="x")

    def test_no_future_dates(self):
        with self.assertRaises(BusinessRuleError):
            self._submit(entry_date=timezone.localdate() + timedelta(days=1))

    def test_hours_must_be_between_0_and_24(self):
        with self.assertRaises(BusinessRuleError):
            self._submit(hours_worked=Decimal("25"))

    def test_only_assigned_mentor_can_sign_off(self):
        entry = self._submit()
        other_mentor = make_mentor()
        with self.assertRaises(NotAllowed):
            sign_off_entry(other_mentor.user, entry)
        sign_off_entry(self.mentor_user, entry)
        entry.refresh_from_db()
        self.assertTrue(entry.mentor_signed_off)

    def test_signed_off_entry_cannot_be_edited(self):
        entry = sign_off_entry(self.mentor_user, self._submit())
        with self.assertRaises(BusinessRuleError):
            edit_entry(self.student_user, entry, hours_worked=Decimal("4"), description="changed")

    def test_reopen_allows_edit_and_is_audited(self):
        entry = sign_off_entry(self.mentor_user, self._submit())
        reopen_entry(self.mentor_user, entry, "Hours look wrong")
        edit_entry(self.student_user, entry, hours_worked=Decimal("6"), description="Corrected")
        self.assertTrue(AuditLog.objects.filter(action__startswith="Reopen logbook entry").exists())
