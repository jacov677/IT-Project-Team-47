# seed_all.py - FULL SEED FOR WHOLE TEAM
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from datetime import date, timedelta
from decimal import Decimal
from django.utils import timezone
from django.core.files.base import ContentFile
from apps.accounts.models import User, Student, Coordinator, Mentor
from apps.organisations.models import HostOrganization
from apps.placements.models import Placement, Document
from apps.logbook.models import LogbookEntry
from apps.assessments.models import Assessment, Evaluation, AssessmentResult
from apps.reports.models import Report

def make_user(username, first, last, email):
    u, _ = User.objects.get_or_create(username=username, defaults={"email": email, "first_name": first, "last_name": last})
    return u

# --- 1. ORGANISATIONS FIRST ---
orgs = []
for name in ["Tech Solutions Durban", "EThekwini Municipality IT", "Nedbank Tech Hub"]:
    o, _ = HostOrganization.objects.get_or_create(organisation_name=name)
    orgs.append(o)

# --- 2. PEOPLE ---
coord = Coordinator.objects.get_or_create(user=make_user("coord_thandi", "Thandi", "Mokoena", "thandi@test.co.za"))[0]
coord2 = Coordinator.objects.get_or_create(user=make_user("coord_nkule", "Nkule", "Zuma", "nkule@test.co.za"))[0]
mentor1 = Mentor.objects.get_or_create(user=make_user("mentor_sipho", "Sipho", "Dube", "sipho@test.co.za"), defaults={"organisation": orgs[0]})[0]
mentor2 = Mentor.objects.get_or_create(user=make_user("mentor_naledi", "Naledi", "Khumalo", "naledi@test.co.za"), defaults={"organisation": orgs[1]})[0]

students_data = [
    ("stu_ayesha", "Ayesha", "Khan", "ayesha@test.co.za"),
    ("stu_lwazi", "Lwazi", "Ndlovu", "lwazi@test.co.za"),
    ("stu_mkhayaristo", "Mkhayaristo", "Cele", "risto@test.co.za"),
    ("stu_bongani", "Bongani", "Zulu", "bongani@test.co.za"),
    ("stu_zanele", "Zanele", "Mthembu", "zanele@test.co.za"),
]
students = []
for idx, (un, fn, ln, em) in enumerate(students_data):
    s, _ = Student.objects.get_or_create(
        user=make_user(un, fn, ln, em),
        defaults={"student_number": f"STU2026{idx+1:03d}"}
    )
    students.append(s)

# --- 3. PLACEMENTS + EVERYTHING LINKED ---
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
            defaults={"hours_worked": Decimal("8.00"), "activities": f"Day {d+1}: Worked on {title} tasks, standup, fixed bugs", "skills_learned": "Django, MySQL, Teamwork", "status": LogbookEntry.Status.SUBMITTED if d>0 else LogbookEntry.Status.DRAFT}
        )
    Assessment.objects.get_or_create(placement=p, student=stu, defaults={"mentor": ment, "score": Decimal("80.00") + i, "feedback": f"Good progress for {stu.user.first_name}", "status": Assessment.Status.SUBMITTED})
    Evaluation.objects.get_or_create(placement=p, mentor=ment, defaults={"score": 80+i, "feedback": "Strong work ethic", "evaluation_date": date.today()})
    AssessmentResult.objects.get_or_create(placement=p, defaults={"coordinator": co, "final_mark": 80+i, "outcome": "PASS"})
    Report.objects.get_or_create(placement=p, student=stu, title=f"{title} - Final Report", defaults={"coordinator": co, "report_type": Report.ReportType.PLACEMENT, "summary": f"Report for {stu.user.first_name} at {org.organisation_name} - {status}", "status": Report.Status.SUBMITTED})

print("DONE FOR WHOLE TEAM")
for m, name in [(Student, "Students"), (Placement, "Placements"), (Document, "Documents"), (LogbookEntry, "Logbook"), (Assessment, "Assessments"), (Evaluation, "Evaluations"), (AssessmentResult, "Results"), (Report, "Reports")]:
    print(f"{name}: {m.objects.count()}")
