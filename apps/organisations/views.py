from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import PlacementOpportunity, HostOrganisation
from .forms import PlacementOpportunityForm

def org_dashboard(request):
    opportunities = PlacementOpportunity.objects.all()
    organisations = HostOrganisation.objects.all()
    context = {
        'opportunities': opportunities,
        'organisations': organisations,
    }
    return render(request, 'organisations/dashboard.html', context)

def add_opportunity(request):
    if request.method == 'POST':
        form = PlacementOpportunityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('org_dashboard')
    else:
        form = PlacementOpportunityForm()
    return render(request, 'organisations/add_opportunity.html', {'form': form})