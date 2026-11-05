from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Student, Coordinator, Mentor

User = get_user_model()


class AccountsModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="student1",
            password="TestPassword123!",
            role=User.Role.STUDENT
        )

    def test_user_role(self):
        self.assertEqual(self.user.role, User.Role.STUDENT)

    def test_student_profile(self):
        student = Student.objects.create(
            student_number="ST001",
            user=self.user,
            first_name="Test",
            last_name="Student",
            qualification="Diploma in IT"
        )
        self.assertEqual(student.user, self.user)

    def test_user_string(self):
        self.assertIn("student1", str(self.user))


class LoginTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="student2",
            email="student2@test.com",
            password="TestPassword123!",
            role=User.Role.STUDENT,
        )

    def test_login_page_loads(self):
        self.assertEqual(self.client.get(reverse("accounts:login")).status_code, 200)

    def test_login_with_email(self):
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "Student2@Test.com", "password": "TestPassword123!"},
        )
        self.assertRedirects(response, reverse("core:home"))

    def test_wrong_password_is_rejected(self):
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "student2@test.com", "password": "wrong"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_inactive_user_cannot_log_in(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "student2@test.com", "password": "TestPassword123!"},
        )
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_accounts_page_needs_login(self):
        response = self.client.get(reverse("accounts:index"))
        self.assertRedirects(response, reverse("accounts:login") + "?next=" + reverse("accounts:index"))

    def test_logout(self):
        self.client.post(
            reverse("accounts:login"),
            {"username": "student2@test.com", "password": "TestPassword123!"},
        )
        response = self.client.post(reverse("accounts:logout"))
        self.assertRedirects(response, reverse("accounts:login"))
