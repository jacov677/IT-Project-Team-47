from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from .decorators import role_required

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
        self.assertRedirects(response, reverse("accounts:dashboard"), fetch_redirect_response=False)

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


class RegistrationTests(TestCase):
    data = {
        "email": "New.Student@Test.com",
        "first_name": "Lerato",
        "last_name": "Nkosi",
        "student_number": "402400001",
        "qualification": "BSc IT",
        "contact_number": "",
        "password1": "Strong-pass-2026!",
        "password2": "Strong-pass-2026!",
    }

    def test_register_page_loads(self):
        self.assertEqual(self.client.get(reverse("accounts:register")).status_code, 200)

    def test_registration_creates_inactive_student(self):
        response = self.client.post(reverse("accounts:register"), self.data)
        self.assertRedirects(response, reverse("accounts:login"))
        user = User.objects.get(email="new.student@test.com")
        self.assertFalse(user.is_active)
        self.assertEqual(user.role, User.Role.STUDENT)
        self.assertEqual(user.student_profile.student_number, "402400001")

    def test_duplicate_email_is_rejected(self):
        self.client.post(reverse("accounts:register"), self.data)
        response = self.client.post(reverse("accounts:register"), {**self.data, "student_number": "999"})
        self.assertContains(response, "already exists")

    def test_waiting_account_gets_clear_message(self):
        self.client.post(reverse("accounts:register"), self.data)
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "new.student@test.com", "password": "Strong-pass-2026!"},
        )
        self.assertContains(response, "waiting for approval")

    def test_can_log_in_after_admin_activates(self):
        self.client.post(reverse("accounts:register"), self.data)
        User.objects.filter(email="new.student@test.com").update(is_active=True)
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "new.student@test.com", "password": "Strong-pass-2026!"},
        )
        self.assertRedirects(response, reverse("accounts:dashboard"), fetch_redirect_response=False)



class RoleRequiredTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        @role_required(User.Role.COORDINATOR, User.Role.ADMIN)
        def protected(request):
            return HttpResponse("ok")

        self.view = protected

    def make_request(self, user):
        request = self.factory.get("/protected/")
        request.user = user
        return request

    def make_user(self, email, role, **extra):
        return User.objects.create_user(username=email, email=email, password="Pass12345!", role=role, **extra)

    def test_anonymous_is_sent_to_login(self):
        response = self.view(self.make_request(AnonymousUser()))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_student_is_forbidden(self):
        user = self.make_user("s@test.com", User.Role.STUDENT)
        with self.assertRaises(PermissionDenied):
            self.view(self.make_request(user))

    def test_coordinator_allowed(self):
        user = self.make_user("c@test.com", User.Role.COORDINATOR)
        self.assertEqual(self.view(self.make_request(user)).status_code, 200)

    def test_admin_allowed(self):
        user = self.make_user("a@test.com", User.Role.ADMIN)
        self.assertEqual(self.view(self.make_request(user)).status_code, 200)

    def test_superuser_always_allowed(self):
        user = self.make_user("su@test.com", User.Role.STUDENT, is_superuser=True)
        self.assertEqual(self.view(self.make_request(user)).status_code, 200)


class DashboardRedirectTests(TestCase):
    def login_as(self, role, **extra):
        email = f"{role.lower()}@test.com"
        User.objects.create_user(username=email, email=email, password="Pass12345!", role=role, **extra)
        self.client.login(email=email, password="Pass12345!")

    def test_anonymous_is_sent_to_login(self):
        response = self.client.get(reverse("accounts:dashboard"))
        self.assertRedirects(response, "/accounts/login/?next=/accounts/dashboard/", fetch_redirect_response=False)

    def test_student_goes_to_placements(self):
        self.login_as(User.Role.STUDENT)
        response = self.client.get(reverse("accounts:dashboard"))
        self.assertRedirects(response, reverse("placements:index"), fetch_redirect_response=False)

    def test_mentor_goes_to_logbook(self):
        self.login_as(User.Role.MENTOR)
        response = self.client.get(reverse("accounts:dashboard"))
        self.assertRedirects(response, reverse("logbook:index"), fetch_redirect_response=False)

    def test_superuser_goes_to_admin(self):
        self.login_as(User.Role.STUDENT, is_superuser=True, is_staff=True)
        response = self.client.get(reverse("accounts:dashboard"))
        self.assertRedirects(response, reverse("admin:index"), fetch_redirect_response=False)

    def test_login_lands_on_dashboard(self):
        User.objects.create_user(username="c@test.com", email="c@test.com", password="Pass12345!", role=User.Role.COORDINATOR)
        response = self.client.post(reverse("accounts:login"), {"username": "c@test.com", "password": "Pass12345!"})
        self.assertRedirects(response, reverse("accounts:dashboard"), fetch_redirect_response=False)
