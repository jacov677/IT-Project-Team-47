
from django.test import TestCase
from .models import HostOrganization


class OrganisationModelTests(TestCase):

    def setUp(self):
        self.organisation = HostOrganization.objects.create(
            organisation_name="Test Organisation",
            industry="Information Technology",
            address="Durban, South Africa",
            contact_email="contact@example.com",
        )

    def test_organisation_creation(self):
        self.assertIsNotNone(self.organisation.organisation_id)
        self.assertEqual(
            self.organisation.organisation_name,
            "Test Organisation",
        )

    def test_organisation_string(self):
        self.assertEqual(
            str(self.organisation),
            "Test Organisation",
        )

    def test_organisation_is_active_by_default(self):
        self.assertTrue(self.organisation.is_active)
