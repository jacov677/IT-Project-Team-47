from django.urls import path
from . import views

urlpatterns = [
    path('', views.org_dashboard, name='org_dashboard'),
    path('add/', views.add_opportunity, name='add_opportunity'),
]