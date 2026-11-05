from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import HostOrganization


@login_required
def index(request):
    context = {
        "total_organisations": HostOrganization.objects.count(),
        "active_organisations": HostOrganization.objects.filter(
            is_active=True
        ).count(),
        "organisations": HostOrganization.objects.all(),
    }

    return render(request, "organisations/index.html", context)
