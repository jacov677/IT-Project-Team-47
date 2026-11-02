from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import Role
from apps.audit.models import AuditLog
from apps.core.testing import PASSWORD, make_student, make_user


class LoginTests(TestCase):
    def test_login_with_email_redirects_to_dashboard(self):
        student = make_student()
        response = self.client.post(reverse("accounts:login"), {"username": student.user.email, "password": PASSWORD})
        self.assertRedirects(response, reverse("core:dashboard"))

    def test_login_is_audited(self):
        student = make_student()
        self.client.post(reverse("accounts:login"), {"username": student.user.email, "password": PASSWORD})
        self.assertTrue(AuditLog.objects.filter(user=student.user, action="Login").exists())

    def test_inactive_account_cannot_log_in(self):
        user = make_user(Role.STUDENT, is_active=False)
        response = self.client.post(reverse("accounts:login"), {"username": user.email, "password": PASSWORD})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertContains(response, "not active yet")

    def test_email_login_is_case_insensitive(self):
        student = make_student()
        response = self.client.post(reverse("accounts:login"),
                                    {"username": student.user.email.upper(), "password": PASSWORD})
        self.assertRedirects(response, reverse("core:dashboard"))

    def test_password_is_stored_as_hash(self):
        user = make_user(Role.STUDENT)
        self.assertNotEqual(user.password, PASSWORD)
        self.assertTrue(user.check_password(PASSWORD))

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("core:dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response.url)
