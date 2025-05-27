from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib import messages

from patient import models as patient_models
from base import models as base_models
import patient


# Create your views here.
@login_required
def dashboard(request):
    patient = patient_models.Patient.objects.get(user=request.user)
    appointments = base_models.Appointment.objects.filter(patient=patient)
    notifications = patient_models.Notification.objects.filter(patient=patient)
    total_spent = base_models.Billing.objects.filter(patient=patient).aggregate(total_spent=models.Sum("total"))["total_spent"]

    context = {
        "patient": patient,
        "appointments": appointments,
        "notifications": notifications,
        "total_spent": total_spent,
    }

    return render(request, "patient/dashboard.html", context)

@login_required
def appointment(request):
    patient = patient_models.Patient.objects.get(user=request.user)
    appointments = base_models.Appointment.objects.filter(patient=patient)

    context= {
        "appointments": appointments,
    }    

    return render(request, "patient/appointment.html", context)

@login_required
def appointment_detail(request, appointment_id):
    patient = patient_models.Patient.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(id=appointment_id, patient=patient)

    medical_records = base_models.MedicalRecord.objects.filter(appointment=appointment)
    lab_tests = base_models.LabTest.objects.filter(appointment=appointment)
    prescriptions = base_models.Prescription.objects.filter(appointment=appointment)    

    context = {
        "appointment": appointment,
        "medical_records": medical_records,
        "lab_tests": lab_tests,
        "prescriptions": prescriptions,
    }
    return render(request, "patient/appointment_detail.html", context)

@login_required
def cancel_appointment(request, appointment_id):
    patient = patient_models.Patient.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(id=appointment_id, patient=patient)
    appointment.status = "Cancelled"
    appointment.save()

    messages.success(request, "Appointment cancelled successfully.")
    return redirect("patient:appointment", appointment_id=appointment_id)

def activate_appointment(request, appointment_id):
    patient = patient_models.Patient.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(id=appointment_id, patient=patient)
    appointment.status = "Scheduled"
    appointment.save()

    messages.success(request, "Appointment Re-Scheduled successfully.")
    return redirect("patient:appointment", appointment_id=appointment_id)


@login_required
def medical_report(request, appointment_id):
    patient = patient_models.Patient.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(id=appointment_id, patient=patient)
    medical_records = base_models.MedicalRecord.objects.filter(appointment=appointment)

    context = {
        "appointment": appointment,
        "medical_records": medical_records,
    }
    return render(request, "patient/medical_report.html", context)

@login_required
def payments(request):
    patient = patient_models.Patient.objects.get(user=request.user)
    payments = base_models.Billing.objects.filter(patient=patient, status="Paid")

    context = { 
        "payments": payments,
    }
    return render(request, "patient/payments.html", context)

@login_required
def notifications(request):
    patient = patient_models.Patient.objects.get(user=request.user)
    notifications = patient_models.Notification.objects.filter(patient=patient)

    context = {
        "notifications": notifications,
    }
    return render(request, "patient/notifications.html", context)

@login_required
def seen_notification(request, id):
    patient = patient_models.models.Patient.objects.get(user=request.user)
    notification = patient_models.models.Notification.objects.get(patient=patient, id=id)
    notification.seen = True
    notification.save()

    messages.success(request, "Notification Seen.")
    return redirect("patient:notifications")


@login_required
def profile(request):
    patient = patient_models.Patient.objects.get(user=request.user)
    formatted_dob = patient.dob.strftime("%Y-%m-%d")
    
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        image = request.FILES.get("image")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")
        dob = request.POST.get("dob")

        if image:
            patient.image = image

        patient.full_name = full_name
        patient.mobile = mobile
        patient.address = address
        patient.dob = dob
        patient.save()

        messages.success(request, "Profile Updated Successfully.")
        return redirect("patient:profile")
    
    context = {
        "patient": patient,
        "formatted_dob": formatted_dob,
    }
    return render(request, "patient/profile.html", context)