from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import redirect, render

from apps.accounts.models import Role, User
from apps.logbook.models import LogbookEntry
from apps.placements.models import Placement, PlacementStatus


def home(request):
    if request.user.is_authenticated:
        return redirect("core:dashboard")
    return redirect("accounts:login")


@login_required
def dashboard(request):
    """Send each user to the dashboard for their role (section 4.7)."""
    handler = {
        Role.STUDENT: _student_dashboard,
        Role.MENTOR: _mentor_dashboard,
        Role.COORDINATOR: _coordinator_dashboard,
        Role.ADMIN: _admin_dashboard,
    }.get(request.user.role)
    if handler is None:
        return render(request, "core/no_profile.html", status=403)
    return handler(request)


def _missing_profile(request):
    return render(request, "core/no_profile.html", status=403)


def _student_dashboard(request):
    student = getattr(request.user, "student", None)
    if student is None:
        return _missing_profile(request)
    placements = student.placements.select_related("organisation", "mentor").all()
    current = placements.filter(status__in=[PlacementStatus.APPROVED, PlacementStatus.ACTIVE]).first()
    recent_entries = LogbookEntry.objects.filter(placement=current)[:5] if current else []
    return render(request, "core/dashboard_student.html", {
        "student": student, "placements": placements, "current": current, "recent_entries": recent_entries,
    })


def _mentor_dashboard(request):
    mentor = getattr(request.user, "mentor", None)
    if mentor is None:
        return _missing_profile(request)
    placements = (mentor.placements.select_related("student")
                  .filter(status__in=[PlacementStatus.APPROVED, PlacementStatus.ACTIVE])
                  .annotate(unsigned=Count("logbook_entries", filter=Q(logbook_entries__mentor_signed_off=False))))
    return render(request, "core/dashboard_mentor.html", {"mentor": mentor, "placements": placements})


def _coordinator_dashboard(request):
    coordinator = getattr(request.user, "coordinator", None)
    if coordinator is None:
        return _missing_profile(request)
    counts = dict(Placement.objects.values_list("status").annotate(n=Count("pk")))
    pending = Placement.objects.filter(status=PlacementStatus.PENDING).select_related("student", "organisation")
    return render(request, "core/dashboard_coordinator.html", {
        "coordinator": coordinator,
        "counts": {label: counts.get(value, 0) for value, label in PlacementStatus.choices},
        "pending": pending,
    })


def _admin_dashboard(request):
    inactive = User.objects.filter(is_active=False).order_by("created_at")
    by_role = dict(User.objects.values_list("role").annotate(n=Count("pk")))
    return render(request, "core/dashboard_admin.html", {
        "inactive": inactive,
        "by_role": {label: by_role.get(value, 0) for value, label in Role.choices},
    })
