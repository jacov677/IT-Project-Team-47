from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import Role
from apps.core.testing import PASSWORD, make_placement, make_student, make_user


class DashboardTests(TestCase):
    def setUp(self):
        self.placement = make_placement()

    def _get_dashboard(self, user):
        self.client.login(email=user.email, password=PASSWORD)
        return self.client.get(reverse("core:dashboard"))

    def test_each_role_sees_its_dashboard(self):
        cases = {
            self.placement.student.user: "core/dashboard_student.html",
            self.placement.mentor.user: "core/dashboard_mentor.html",
            self.placement.coordinator.user: "core/dashboard_coordinator.html",
            make_user(Role.ADMIN): "core/dashboard_admin.html",
        }
        for user, template in cases.items():
            with self.subTest(role=user.role):
                response = self._get_dashboard(user)
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template)
                self.client.logout()

    def test_student_cannot_view_another_students_placement(self):
        other = make_student()
        self.client.login(email=other.user.email, password=PASSWORD)
        response = self.client.get(reverse("placements:detail", args=[self.placement.pk]))
        self.assertEqual(response.status_code, 403)

    def test_assigned_mentor_can_view_placement(self):
        self.client.login(email=self.placement.mentor.user.email, password=PASSWORD)
        response = self.client.get(reverse("placements:detail", args=[self.placement.pk]))
        self.assertEqual(response.status_code, 200)
