from django.urls import path
from . import views

app_name = 'organisations'

urlpatterns = [
    path('', views.org_dashboard, name='org_dashboard'),

    path('', views.org_dashboard, name='index'),

    path('add-opportunity/', views.add_opportunity, name='add_opportunity'),
]