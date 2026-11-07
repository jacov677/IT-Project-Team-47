from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PlacementOpportunity, HostOrganization
from .forms import PlacementOpportunityForm


@login_required
def org_dashboard(request):
    organization = HostOrganization.objects.filter(owner=request.user).first()
    opportunities = organization.opportunities.all() if organization else []

    context = {
        'organization': organization,
        'opportunities': opportunities,
    }
    return render(request, 'organisations/dashboard.html', context)


@login_required
def add_opportunity(request):
    organization = HostOrganization.objects.filter(owner=request.user).first()
    if organization is None:
        raise Http404("No host organisation is linked to your account.")

    if request.method == 'POST':
        form = PlacementOpportunityForm(request.POST)
        if form.is_valid():
            opportunity = form.save(commit=False)
            opportunity.organisation = organization
            opportunity.save()
            return redirect('organisations:org_dashboard')
    else:
        form = PlacementOpportunityForm()

    return render(request, 'organisations/add_opportunity.html', {'form': form})