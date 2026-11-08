from django.test import TestCase
from django.urls import reverse


class LogbookPageTests(TestCase):
    def test_index_page_loads(self):
        response = self.client.get(reverse("logbook:index"))
        self.assertEqual(response.status_code, 302)
