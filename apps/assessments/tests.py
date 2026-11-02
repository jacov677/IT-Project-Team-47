from django.test import TestCase
from django.urls import reverse


class AssessmentsPageTests(TestCase):
    def test_index_page_loads(self):
        response = self.client.get(reverse("assessments:index"))
        self.assertEqual(response.status_code, 200)
