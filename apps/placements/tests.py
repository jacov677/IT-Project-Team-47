from django.test import TestCase
from django.urls import reverse


class PlacementsPageTests(TestCase):
    def test_index_page_loads(self):
        response = self.client.get(reverse("placements:index"))
        self.assertEqual(response.status_code, 200)
