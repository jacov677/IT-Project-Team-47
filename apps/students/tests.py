from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.accounts.models import Student, User
from apps.organisations.models import HostOrganization, PlacementOpportunity
from .models import Application, Notification

PASSWORD = "Pass12345!"
LETTER = "I would love to join your team because I enjoy building web systems."


class StudentPortalTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="s@test.com", email="s@test.com", password=PASSWORD,
            first_name="Sam", last_name="Student", role=User.Role.STUDENT,
        )
        self.student = Student.objects.create(
            student_number="STU001", user=self.user, first_name="Sam", last_name="Student",
            qualification="BSc IT",
        )
        self.org = HostOrganization.objects.create(
            organisation_name="Tech Co", industry="IT", address="Durban", contact_email="hr@tech.co.za",
        )
        self.opportunity = PlacementOpportunity.objects.create(
            organisation=self.org, title="Junior Developer", description="Build Django apps",
            closing_date=timezone.localdate() + timedelta(days=10),
        )
        self.client.login(email="s@test.com", password=PASSWORD)


class AccessTests(StudentPortalTestCase):
    def test_student_sees_dashboard(self):
        response = self.client.get(reverse("students:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Junior Developer")

    def test_anonymous_is_sent_to_login(self):
        self.client.logout()
        response = self.client.get(reverse("students:dashboard"))
        self.assertRedirects(response, reverse("accounts:login") + "?next=" + reverse("students:dashboard"),
                             fetch_redirect_response=False)

    def test_coordinator_is_turned_away(self):
        User.objects.create_user(username="c@test.com", email="c@test.com", password=PASSWORD,
                                 role=User.Role.COORDINATOR)
        self.client.login(email="c@test.com", password=PASSWORD)
        response = self.client.get(reverse("students:dashboard"))
        self.assertRedirects(response, reverse("core:home"), fetch_redirect_response=False)

    def test_all_pages_load(self):
        for name in ["dashboard", "profile", "profile_edit", "opportunities", "application_list", "notifications"]:
            self.assertEqual(self.client.get(reverse(f"students:{name}")).status_code, 200, name)
        url = reverse("students:opportunity_detail", args=[self.opportunity.pk])
        self.assertEqual(self.client.get(url).status_code, 200)


class ApplicationTests(StudentPortalTestCase):
    def apply(self):
        url = reverse("students:opportunity_detail", args=[self.opportunity.pk])
        return self.client.post(url, {"cover_letter": LETTER})

    def test_apply_creates_application_and_notification(self):
        response = self.apply()
        self.assertRedirects(response, reverse("students:application_list"), fetch_redirect_response=False)
        self.assertEqual(Application.objects.filter(student=self.student).count(), 1)
        self.assertTrue(Notification.objects.filter(user=self.user, title="Application submitted").exists())

    def test_cannot_apply_twice(self):
        self.apply()
        self.apply()
        self.assertEqual(Application.objects.count(), 1)

    def test_cannot_apply_after_closing_date(self):
        self.opportunity.closing_date = timezone.localdate() - timedelta(days=1)
        self.opportunity.save()
        self.apply()
        self.assertEqual(Application.objects.count(), 0)

    def test_withdraw(self):
        self.apply()
        application = Application.objects.get()
        self.client.post(reverse("students:application_withdraw", args=[application.pk]))
        application.refresh_from_db()
        self.assertEqual(application.status, Application.Status.WITHDRAWN)

    def test_status_change_notifies_student(self):
        self.apply()
        application = Application.objects.get()
        application.status = Application.Status.APPROVED
        application.save()
        self.assertTrue(Notification.objects.filter(user=self.user, title="Application approved").exists())


class ProfileTests(StudentPortalTestCase):
    def test_edit_profile_updates_student_record(self):
        response = self.client.post(reverse("students:profile_edit"), {
            "first_name": "Samuel", "last_name": "Student", "email": "s@test.com",
            "qualification": "BSc Information Technology", "contact_number": "0821234567",
            "year_of_study": 3, "skills": "Python, Django", "bio": "Final year student",
        })
        self.assertRedirects(response, reverse("students:profile"), fetch_redirect_response=False)
        self.student.refresh_from_db()
        self.assertEqual(self.student.first_name, "Samuel")
        self.assertEqual(self.student.qualification, "BSc Information Technology")
        self.assertEqual(self.student.portal_profile.skills_list, ["Python", "Django"])
