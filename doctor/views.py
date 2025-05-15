from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from doctor import models as doctor_models
from base import models as base_models

# Create your views here.

@login_required
def dashboard(request):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointments = base_models.Appointment.objects.filter(doctor=doctor)
    notifications = doctor_models.Notification.objects.filter(doctor=doctor)

    context  = {
        'appointments': appointments,
        'notifications': notifications, 
    }