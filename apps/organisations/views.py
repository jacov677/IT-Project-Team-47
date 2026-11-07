from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PlacementOpportunity, HostOrganization
from .forms import PlacementOpportunityForm

@login_required
def org_dashboard(request):
    # Get the organization linked to the currently logged-in user (Organisation-specific permission)
    try:
        organization = HostOrganization.objects.get(user=request.user)
        opportunities = organization.opportunities.all()
    except HostOrganization.DoesNotExist:
        organization = None
        opportunities = []

    context = {
        'organization': organization,
        'opportunities': opportunities,
    }
    return render(request, 'organisations/dashboard.html', context)


@login_required
def add_opportunity(request):
    organization = get_object_or_404(HostOrganization, user=request.user)

    if request.method == 'POST':
        form = PlacementOpportunityForm(request.POST)
        if form.is_valid():
            opportunity = form.save(commit=False)
            opportunity.organisation = organization  # Automatically bind to logged-in employer
            opportunity.save()
            return redirect('organisations:org_dashboard')
    else:
        form = PlacementOpportunityForm()

    return render(request, 'organisations/add_opportunity.html', {'form': form})