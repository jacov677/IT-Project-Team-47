from django.test import TestCase
from django.urls import reverse


class HomePageTests(TestCase):
    def test_home_page_lists_every_module(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        for name in ["Accounts", "Organisations", "Placements", "Logbook", "Assessments", "Reports"]:
            self.assertContains(response, name)
