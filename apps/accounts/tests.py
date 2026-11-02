from django.test import TestCase
from django.urls import reverse


class AccountsPageTests(TestCase):
    def test_index_page_loads(self):
        response = self.client.get(reverse("accounts:index"))
        self.assertEqual(response.status_code, 200)
