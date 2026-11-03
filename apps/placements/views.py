
from django.shortcuts import render


def index(request):
    return render(request, "placements/index.html")


def placement_list(request):
    return render(request, "placements/placement_list.html")
def placement_detail(request):
    return render(request, "placements/placement_detail.html")
def placement_create(request):
    return render(request, "placements/placement_form.html")
def document_list(request):
    return render(request, "placements/document_list.html")