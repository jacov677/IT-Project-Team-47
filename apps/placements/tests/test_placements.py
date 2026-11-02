import shutil
import tempfile
from datetime import timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from apps.audit.models import AuditLog
from apps.core.exceptions import BusinessRuleError, NotAllowed
from apps.core.testing import PASSWORD, make_coordinator, make_mentor, make_placement, make_student
from apps.placements.models import Document, PlacementStatus
from apps.placements.services import approve_placement, create_placement


class CreatePlacementTests(TestCase):
    def setUp(self):
        self.coordinator = make_coordinator()
        self.mentor = make_mentor()
        self.student = make_student()
        self.today = timezone.localdate()

    def _create(self, **overrides):
        data = dict(user=self.coordinator.user, student=self.student, organisation=self.mentor.organisation,
                    mentor=self.mentor, coordinator=self.coordinator,
                    start_date=self.today, end_date=self.today + timedelta(days=90))
        data.update(overrides)
        return create_placement(**data)

    def test_creates_pending_placement_and_audits_it(self):
        placement = self._create()
        self.assertEqual(placement.status, PlacementStatus.PENDING)
        self.assertTrue(AuditLog.objects.filter(table_name="placement", record_id=str(placement.pk)).exists())

    def test_student_cannot_have_two_open_placements(self):
        self._create()
        with self.assertRaises(BusinessRuleError):
            self._create()

    def test_mentor_must_belong_to_organisation(self):
        other_mentor = make_mentor()
        with self.assertRaises(BusinessRuleError):
            self._create(mentor=other_mentor)

    def test_end_date_must_be_after_start(self):
        with self.assertRaises(BusinessRuleError):
            self._create(end_date=self.today)


class ApprovePlacementTests(TestCase):
    def test_coordinator_approves_pending_placement(self):
        placement = make_placement(status=PlacementStatus.PENDING)
        approved = approve_placement(placement, placement.coordinator.user)
        self.assertEqual(approved.status, PlacementStatus.APPROVED)
        self.assertIsNotNone(approved.approved_at)

    def test_only_coordinator_can_approve(self):
        placement = make_placement(status=PlacementStatus.PENDING)
        with self.assertRaises(NotAllowed):
            approve_placement(placement, placement.student.user)

    def test_cannot_approve_second_placement_for_same_student(self):
        active = make_placement(status=PlacementStatus.ACTIVE)
        second = make_placement(status=PlacementStatus.PENDING, student=active.student)
        with self.assertRaises(BusinessRuleError):
            approve_placement(second, second.coordinator.user)


TEMP_MEDIA = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class DocumentAccessTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.placement = make_placement()
        self.document = Document.objects.create(
            placement=self.placement, document_type="Placement agreement",
            file_path=SimpleUploadedFile("agreement.pdf", b"%PDF-1.4 test", content_type="application/pdf"),
        )
        self.url = reverse("placements:download_document", args=[self.document.pk])

    def test_owner_can_download(self):
        self.client.login(email=self.placement.student.user.email, password=PASSWORD)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(AuditLog.objects.filter(action="Download document").exists())

    def test_other_student_is_blocked(self):
        other = make_student()
        self.client.login(email=other.user.email, password=PASSWORD)
        self.assertEqual(self.client.get(self.url).status_code, 403)

    def test_uploaded_file_is_renamed(self):
        self.assertNotIn("agreement", self.document.file_path.name)
