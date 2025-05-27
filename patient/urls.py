from django.urls import path
from patient import views

app_name = "patient"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("appointment/", views.appointment, name="appointment"),
    path("appointment/<int:appointment_id>", views.appointment_detail, name="appointment_detail"),

    path("cancel_appointment/<int:appointment_id>", views.cancel_appointment, name="cancel_appointment"),
    path("activate_appointment/<int:appointment_id>", views.activate_appointment, name="activate_appointment"),

    path("medical_report/<int:appointment_id>", views.medical_report, name="medical_report"),

    path("payments/", views.payments, name="payments"),
    path("notifications/", views.notifications, name="notifications"),
    path("seen_notification/<int:id>", views.seen_notification, name="seen_notification"),

    path("profile/", views.profile, name="profile"),
]
