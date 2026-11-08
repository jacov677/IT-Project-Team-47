from django.urls import path

from . import views

app_name = "assessments"

urlpatterns = [
    path("", views.index, name="index"),
    path("manage/", views.assessment_list, name="assessment_list"),
    path("details/", views.assessment_detail, name="assessment_detail"),
    path("capture-result/", views.result_capture, name="result_capture"),
    path("history/", views.assessment_history, name="assessment_history"),
]