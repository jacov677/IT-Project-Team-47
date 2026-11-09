from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from apps.accounts.models import User
from apps.organisations.models import PlacementOpportunity
from .forms import ApplicationForm, ProfileUpdateForm, StudentDetailsForm, UserUpdateForm
from .models import Application, StudentPortalProfile


def student_required(view):
    """Login required AND the user must be a student with a Student record.

    Sets request.student (accounts.Student) and request.portal (StudentPortalProfile).
    """
    @wraps(view)
    @login_required
    def wrapper(request, *args, **kwargs):
        student = getattr(request.user, "student_profile", None)
        if request.user.role != User.Role.STUDENT or student is None:
            messages.error(request, "This area is for students only.")
            return redirect("core:home")
        request.student = student
        request.portal, _ = StudentPortalProfile.objects.get_or_create(student=student)
        return view(request, *args, **kwargs)
    return wrapper


def open_opportunities():
    today = timezone.localdate()
    return (
        PlacementOpportunity.objects
        .filter(is_active=True, organisation__is_active=True)
        .filter(Q(closing_date__isnull=True) | Q(closing_date__gte=today))
        .select_related("organisation")
        .order_by("closing_date", "-created_at")
    )


def is_open(opportunity):
    return opportunity.is_active and (
        opportunity.closing_date is None or opportunity.closing_date >= timezone.localdate()
    )


# ---------- Dashboard ----------
@student_required
def dashboard(request):
    apps = request.student.applications.select_related("opportunity__organisation")
    ctx = {
        "profile": request.portal,
        "total": apps.count(),
        "pending": apps.filter(status__in=[Application.Status.PENDING, Application.Status.UNDER_REVIEW]).count(),
        "approved": apps.filter(status=Application.Status.APPROVED).count(),
        "rejected": apps.filter(status=Application.Status.REJECTED).count(),
        "recent_applications": apps[:5],
        "latest_opportunities": open_opportunities().exclude(applications__student=request.student)[:4],
        "recent_notifications": request.user.notifications.all()[:4],
    }
    return render(request, "students/dashboard.html", ctx)


# ---------- Profile ----------
@student_required
def profile_view(request):
    return render(request, "students/profile.html", {"profile": request.portal})


@student_required
def profile_edit(request):
    data, files = request.POST or None, request.FILES or None
    user_form = UserUpdateForm(data, instance=request.user)
    student_form = StudentDetailsForm(data, instance=request.student)
    profile_form = ProfileUpdateForm(data, files, instance=request.portal)
    forms_ok = request.method == "POST" and all(
        [user_form.is_valid(), student_form.is_valid(), profile_form.is_valid()]
    )
    if forms_ok:
        student_form.save()
        profile_form.save()
        user_form.save()  # last, so it also copies the new name onto the Student record
        messages.success(request, "Your profile has been updated.")
        return redirect("students:profile")
    return render(request, "students/profile_edit.html", {
        "user_form": user_form, "student_form": student_form,
        "profile_form": profile_form, "profile": request.portal,
    })


# ---------- Opportunities & applying ----------
@student_required
def opportunity_list(request):
    qs = open_opportunities()
    q = request.GET.get("q", "").strip()
    industry = request.GET.get("industry", "").strip()
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(organisation__organisation_name__icontains=q) |
                       Q(organisation__industry__icontains=q) | Q(description__icontains=q))
    if industry:
        qs = qs.filter(organisation__industry__iexact=industry)
    page = Paginator(qs, 9).get_page(request.GET.get("page"))
    return render(request, "students/opportunity_list.html", {
        "page": page, "q": q, "industry": industry,
        "industries": open_opportunities().values_list("organisation__industry", flat=True)
                                          .distinct().order_by("organisation__industry"),
        "applied_ids": set(request.student.applications.values_list("opportunity_id", flat=True)),
    })


@student_required
def opportunity_detail(request, pk):
    """Shows an opportunity and handles the application submission (POST)."""
    opportunity = get_object_or_404(PlacementOpportunity.objects.select_related("organisation"), pk=pk)
    existing = request.student.applications.filter(opportunity=opportunity).first()
    form = ApplicationForm(request.POST or None)
    still_open = is_open(opportunity)

    if request.method == "POST":
        if existing:
            messages.warning(request, "You have already applied for this opportunity.")
        elif not still_open:
            messages.error(request, "Applications for this opportunity are closed.")
        elif form.is_valid():
            application = form.save(commit=False)
            application.student = request.student
            application.opportunity = opportunity
            application.save()
            messages.success(request, "Your application has been submitted.")
            return redirect("students:application_list")
    return render(request, "students/opportunity_detail.html", {
        "opportunity": opportunity, "form": form, "existing": existing,
        "profile": request.portal, "is_open": still_open,
    })


# ---------- Application history ----------
@student_required
def application_list(request):
    qs = request.student.applications.select_related("opportunity__organisation")
    status = request.GET.get("status", "")
    if status in Application.Status.values:
        qs = qs.filter(status=status)
    return render(request, "students/application_list.html", {
        "applications": qs, "status": status, "statuses": Application.Status.choices,
    })


@student_required
@require_POST
def application_withdraw(request, pk):
    application = get_object_or_404(Application, pk=pk, student=request.student)
    if application.can_withdraw:
        application.status = Application.Status.WITHDRAWN
        application.save()
        messages.info(request, "Your application has been withdrawn.")
    else:
        messages.error(request, "This application can no longer be withdrawn.")
    return redirect("students:application_list")


# ---------- Notifications ----------
@student_required
def notification_list(request):
    page = Paginator(request.user.notifications.all(), 15).get_page(request.GET.get("page"))
    return render(request, "students/notification_list.html", {"page": page})


@student_required
@require_POST
def notification_mark_read(request, pk):
    request.user.notifications.filter(pk=pk).update(is_read=True)
    next_url = request.POST.get("next", "")
    if not next_url.startswith("/") or next_url.startswith("//"):
        next_url = "students:notifications"
    return redirect(next_url)


@student_required
@require_POST
def notification_mark_all_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    messages.success(request, "All notifications marked as read.")
    return redirect("students:notifications")
