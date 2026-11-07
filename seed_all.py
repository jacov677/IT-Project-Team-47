# seed_all.py
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from datetime import date, timedelta
from decimal import Decimal
from django.utils import timezone
from django.core.files.base import ContentFile
from django.conf import settings
from django.db import transaction

if not settings.DEBUG:
    raise SystemExit("Seed data is for development only")

from apps.accounts.models import User, Student, Coordinator, Mentor
from apps.organisations.models import HostOrganization
from apps.placements.models import Placement, Document
from apps.logbook.models import LogbookEntry
from apps.assessments.models import Assessment, Evaluation, AssessmentResult
from apps.reports.models import Report

def make_user(first, last, email, role):
    # Lookup by EMAIL fixes the duplicate error in your screenshot
    u, created = User.objects.get_or_create(
        email=email,
        defaults={"username": email, "first_name": first, "last_name": last, "role": role},
    )
    if created:
        u.set_password("Test@12345")
        u.save()
    else:
        # Fix old users created with coord_thandi / stu_ayesha usernames
        changed = False
        if u.username != email:
            u.username = email; changed = True
        if u.role != role:
            u.role = role; changed = True
        if not u.has_usable_password():
            u.set_password("Test@12345"); changed = True
        if changed:
            u.save()
    return u

with transaction.atomic():
    orgs = []
    for name in ["Tech Solutions Durban", "EThekwini Municipality IT", "Nedbank Tech Hub"]:
        o, _ = HostOrganization.objects.get_or_create(organisation_name=name)
        orgs.append(o)

    make_user("Admin", "User", "admin@test.co.za", User.Role.ADMIN)

    coord = Coordinator.objects.get_or_create(user=make_user("Thandi", "Mokoena", "thandi@test.co.za", User.Role.COORDINATOR))[0]
    coord2 = Coordinator.objects.get_or_create(user=make_user("Nkule", "Zuma", "nkule@test.co.za", User.Role.COORDINATOR))[0]
    mentor1 = Mentor.objects.get_or_create(user=make_user("Sipho", "Dube", "sipho@test.co.za", User.Role.MENTOR), defaults={"organisation": orgs[0]})[0]
    mentor2 = Mentor.objects.get_or_create(user=make_user("Naledi", "Khumalo", "naledi@test.co.za", User.Role.MENTOR), defaults={"organisation": orgs[1]})[0]

    students_data = [
        ("Ayesha", "Khan", "ayesha@test.co.za"),
        ("Lwazi", "Ndlovu", "lwazi@test.co.za"),
        ("Mkhayaristo", "Cele", "risto@test.co.za"),
        ("Bongani", "Zulu", "bongani@test.co.za"),
        ("Zanele", "Mthembu", "zanele@test.co.za"),
    ]
    students = []
    for idx, (fn, ln, em) in enumerate(students_data):
        s, _ = Student.objects.get_or_create(
            user=make_user(fn, ln, em, User.Role.STUDENT),
            defaults={
                "student_number": f"STU2026{idx+1:03d}",
                "first_name": fn,
                "last_name": ln,
                "qualification": "Diploma in IT",
                "contact_number": f"082000000{idx+1}",
            }
        )
        students.append(s)

    placements_info = [
        (students[0], orgs[0], mentor1, coord, "Software Dev Intern", Placement.Status.APPROVED),
        (students[1], orgs[1], mentor2, coord, "IT Support Intern", Placement.Status.ACTIVE),
        (students[2], orgs[0], mentor1, coord2, "Data Analyst Intern", Placement.Status.PENDING),
        (students[3], orgs[2], mentor2, coord, "Network Intern", Placement.Status.COMPLETED),
        (students[4], orgs[1], mentor1, coord2, "Web Dev Intern", Placement.Status.ACTIVE),
    ]

    for i, (stu, org, ment, co, title, status) in enumerate(placements_info):
        p, _ = Placement.objects.get_or_create(
            student=stu, organisation=org, title=title,
            defaults={"mentor": ment, "coordinator": co, "description": f"WIL Placement - {title}",
                      "start_date": date.today() - timedelta(days=30),
                      "end_date": date.today() + timedelta(days=150),
                      "status": status, "approved_at": timezone.now() if status != Placement.Status.PENDING else None}
        )
        doc, _ = Document.objects.get_or_create(placement=p, title=f"CV - {stu.user.first_name}", defaults={"document_type": Document.DocType.CV})
        if not doc.file_path:
            doc.file_path.save("cv.txt", ContentFile(b"Test CV"), save=True)
        Document.objects.get_or_create(placement=p, title=f"Contract - {stu.user.first_name}", defaults={"document_type": Document.DocType.CONTRACT})

        for d in [0, 1, 2]:
            LogbookEntry.objects.get_or_create(
                placement=p, student=stu, date=date.today() - timedelta(days=d),
                defaults={"hours_worked": Decimal("8.00"), "activities": f"Day {d+1}: Worked on {title} tasks", "skills_learned": "Django, MySQL, Teamwork", "status": LogbookEntry.Status.SUBMITTED if d>0 else LogbookEntry.Status.DRAFT}
            )
        Assessment.objects.get_or_create(placement=p, student=stu, defaults={"mentor": ment, "score": Decimal("80.00") + i, "feedback": f"Good progress for {stu.user.first_name}", "status": Assessment.Status.SUBMITTED})
        Evaluation.objects.get_or_create(placement=p, mentor=ment, defaults={"score": 80+i, "feedback": "Strong work ethic", "evaluation_date": date.today()})
        AssessmentResult.objects.get_or_create(placement=p, defaults={"coordinator": co, "final_mark": 80+i, "outcome": "PASS"})
        Report.objects.get_or_create(placement=p, student=stu, title=f"{title} - Final Report", defaults={"coordinator": co, "report_type": Report.ReportType.PLACEMENT, "summary": f"Report for {stu.user.first_name} at {org.organisation_name} - {status}", "status": Report.Status.SUBMITTED})

    print("DONE FOR WHOLE TEAM")
    for m, name in [(Student, "Students"), (Placement, "Placements"), (Document, "Documents"), (LogbookEntry, "Logbook"), (Assessment, "Assessments"), (Evaluation, "Evaluations"), (AssessmentResult, "Results"), (Report, "Reports")]:
        print(f"{name}: {m.objects.count()}")

