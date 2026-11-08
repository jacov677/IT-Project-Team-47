
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.accounts.decorators import role_required
from apps.accounts.models import User

from .forms import PlacementForm, DocumentForm
from .models import Placement, Document


@role_required(User.Role.COORDINATOR, User.Role.ADMIN)
def index(request):
    placements = Placement.objects.select_related(
        "student",
        "organisation",
        "mentor",
    )

    context = {
        "total_placements": placements.count(),
        "pending_count": placements.filter(
            status=Placement.Status.PENDING
        ).count(),
        "active_count": placements.filter(
            status=Placement.Status.ACTIVE
        ).count(),
        "completed_count": placements.filter(
            status=Placement.Status.COMPLETED
        ).count(),
        "recent_placements": placements[:5],
    }

    return render(request, "placements/index.html", context)


@role_required(User.Role.COORDINATOR, User.Role.ADMIN)
def placement_list(request):
    placements = Placement.objects.select_related(
        "student",
        "organisation",
        "mentor",
    )

    search_query = request.GET.get("q", "").strip()
    status_filter = request.GET.get("status", "").strip()

    if search_query:
        placements = placements.filter(
            Q(title__icontains=search_query)
            | Q(student__first_name__icontains=search_query)
            | Q(student__last_name__icontains=search_query)
            | Q(student__student_number__icontains=search_query)
            | Q(organisation__organisation_name__icontains=search_query)
        )

    if status_filter in Placement.Status.values:
        placements = placements.filter(status=status_filter)
    else:
        status_filter = ""

    all_placements = Placement.objects.all()

    context = {
        "placements": placements,
        "search_query": search_query,
        "status_filter": status_filter,
        "status_choices": Placement.Status.choices,
        "pending_count": all_placements.filter(
            status=Placement.Status.PENDING
        ).count(),
        "approved_count": all_placements.filter(
            status=Placement.Status.APPROVED
        ).count(),
        "active_count": all_placements.filter(
            status=Placement.Status.ACTIVE
        ).count(),
        "completed_count": all_placements.filter(
            status=Placement.Status.COMPLETED
        ).count(),
    }

    return render(request, "placements/placement_list.html", context)


@role_required(User.Role.COORDINATOR, User.Role.ADMIN)
def placement_detail(request, pk):
    placement = get_object_or_404(
        Placement.objects.select_related(
            "student",
            "organisation",
            "mentor",
            "coordinator",
        ),
        pk=pk,
    )

    documents = placement.documents.all()

    context = {
        "placement": placement,
        "documents": documents,
    }

    return render(request, "placements/placement_detail.html", context)


@role_required(User.Role.COORDINATOR, User.Role.ADMIN)
def placement_create(request):
    if request.method == "POST":
        form = PlacementForm(request.POST)

        if form.is_valid():
            placement = form.save()

            messages.success(
                request,
                "Placement created successfully.",
            )

            return redirect(
                "placements:placement_detail",
                pk=placement.pk,
            )
    else:
        form = PlacementForm()

    return render(
        request,
        "placements/placement_form.html",
        {"form": form},
    )


@role_required(User.Role.COORDINATOR, User.Role.ADMIN)
def document_list(request):
    documents = Document.objects.select_related(
        "placement",
        "placement__student",
        "placement__organisation",
    )

    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            placement = form.cleaned_data.get("placement")

            if placement is None:
                form.add_error(
                    "placement",
                    "Please select a placement for this document.",
                )
            else:
                document = form.save(commit=False)
                document.placement = placement
                document.save()

                messages.success(
                    request,
                    "Document uploaded successfully.",
                )

                return redirect("placements:document_list")

    else:
        form = DocumentForm()

    today = timezone.localdate()

    context = {
        "documents": documents,
        "form": form,
        "total_documents": documents.count(),
        "documents_today": documents.filter(
            uploaded_at__date=today
        ).count(),
    }

    return render(request, "placements/document_list.html", context)


@role_required(User.Role.COORDINATOR, User.Role.ADMIN)
def add_document(request, pk):
    placement = get_object_or_404(Placement, pk=pk)

    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            document = form.save(commit=False)
            document.placement = placement
            document.save()

            messages.success(
                request,
                "Document uploaded successfully.",
            )

            return redirect(
                "placements:placement_detail",
                pk=placement.pk,
            )

    else:
        form = DocumentForm(initial={"placement": placement})

    today = timezone.localdate()

    context = {
        "form": form,
        "placement": placement,
        "documents": placement.documents.all(),
        "total_documents": placement.documents.count(),
        "documents_today": placement.documents.filter(
            uploaded_at__date=today
        ).count(),
    }

    return render(request, "placements/document_list.html", context)
