from django.test import TestCase
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
