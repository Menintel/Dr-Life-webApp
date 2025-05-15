from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from patient.models import models as patient_models
from base import models as base_models

# Create your views here.
def dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_doctor:
            return redirect("doctor:dashboard")
        elif request.user.is_patient:
            patient = patient_models.Patient.objects.get(user=request.user)
            context = {
                "patient": patient
            }
            return render(request, "patient/dashboard.html", context)
        else:
            return redirect("base:home")
    else:
        return redirect("base:home")