from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, render

from apps.audit.services import log_action

from .models import Document, Placement
from .services import user_can_view_placement


@login_required
def placement_detail(request, pk):
    placement = get_object_or_404(
        Placement.objects.select_related("student", "organisation", "mentor", "coordinator"), pk=pk
    )
    if not user_can_view_placement(request.user, placement):
        raise PermissionDenied
    return render(request, "placements/placement_detail.html", {
        "placement": placement,
        "documents": placement.documents.all(),
        "entries": placement.logbook_entries.all(),
    })


@login_required
def download_document(request, pk):
    """Documents are never served from a public URL; every download is checked here (4.4.8)."""
    document = get_object_or_404(Document.objects.select_related("placement__student", "placement__mentor"), pk=pk)
    if not user_can_view_placement(request.user, document.placement):
        raise PermissionDenied
    try:
        handle = document.file_path.open("rb")
    except FileNotFoundError as exc:
        raise Http404("File not found.") from exc
    log_action(request.user, "Download document", document)
    return FileResponse(handle, as_attachment=True, filename=document.filename)
