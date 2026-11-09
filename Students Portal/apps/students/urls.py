from django.urls import path

from . import views

app_name = "students"

# Login, logout and registration are handled by the accounts app (accounts:login, accounts:register).
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),

    path("opportunities/", views.opportunity_list, name="opportunities"),
    path("opportunities/<int:pk>/", views.opportunity_detail, name="opportunity_detail"),

    path("applications/", views.application_list, name="application_list"),
    path("applications/<int:pk>/withdraw/", views.application_withdraw, name="application_withdraw"),

    path("notifications/", views.notification_list, name="notifications"),
    path("notifications/<int:pk>/read/", views.notification_mark_read, name="notification_read"),
    path("notifications/read-all/", views.notification_mark_all_read, name="notifications_read_all"),
]
