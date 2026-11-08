
from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User


class AssessmentsPageTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testcoordinator",
            email="coordinator@example.com",
            password="TestPassword123!",
            role=User.Role.COORDINATOR,
        )
        self.client.force_login(self.user)

    def test_index_page_loads(self):
        response = self.client.get(reverse("assessments:index"))
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_user_is_redirected(self):
        self.client.logout()
        response = self.client.get(reverse("assessments:index"))
        self.assertEqual(response.status_code, 302)
