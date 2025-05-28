from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import JsonResponse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

import requests
import stripe

from base import models as base_models
from doctor import models as doctor_models
from patient import models as patient_models

# Create your views here.

def index(request):
    services = base_models.Service.objects.all()
    context = {
        "services":services
    }
    return render(request, "base/index.html", context)

def service_detail(request, service_id):
    service = base_models.Service.objects.get(id=service_id)
    context = {
        "service" : service
    }
    return render(request, "base/service_detail.html", context)


@login_required
def book_appointment(request, service_id, doctor_id):

    service = base_models.Service.objects.get(id=service_id)
    doctor = doctor_models.Doctor.objects.get(id=doctor_id)
    patient =  patient_models.Patient.objects.get(user=request.user)

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        gender = request.POST.get("gender")
        address = request.POST.get("address")
        dob = request.POST.get("dob")
        issues = request.POST.get("issues")
        symptoms = request.POST.get("symptoms")

        #Update Patient bio data
        patient.user.first_name = first_name
        patient.user.last_name = last_name
        patient.email = email
        patient.dob = dob
        patient.mobile = mobile
        patient.gender = gender
        patient.address = address
        patient.save()
        
        # Create appointement Object
        appointment = base_models.Appointment.objects.create (
            service = service,
            doctor = doctor,
            patient = patient,
            appointment_date = doctor.next_available_appointment_date,
            issues = issues,
            symptoms = symptoms,
        )

        billing = base_models.Billing()
        billing.patient = patient
        billing.appointment = appointment
        billing.sub_total = appointment.service.cost
        billing.tax = appointment.service.cost * 5 / 100
        billing.total = billing.sub_total + billing.tax
        billing.status = "Unpaid"
        billing.save()
        
        return redirect("base:checkout", billing.billing_id)

    context = {
        "service":service,
        "doctor":doctor,
        "patient":patient,
    }

    return render(request, "base/book_appointment.html", context)

@login_required
def checkout(request, billing_id):
    billing = base_models.Billing.objects.get(billing_id=billing_id)


    context = {
        "billing":billing,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,

        "paypal_client_id": settings.PAYPAL_CLIENT_ID,
    }

    return render(request, "base/checkout.html", context)

@csrf_exempt
def stripe_payment(request, billing_id):
    billing = base_models.Billing.objects.get(billing_id=billing_id)
    stripe.api_key = settings.STRIPE_SECRET_KEY

    checkout_session = stripe.checkout.Session.create(
        customer_email=billing.patient.email,
        payment_method_types=['card'],
        line_items=[{
                'price_data':{
                    'currency':'USD',
                    'product_data':
                        { 'name':billing.patient.full_name },
                    'unit_amount':int(billing.total) * 100
                },
                'quantity':1,
            }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse("base:stripe_payment_verify", args=[billing.billing_id])) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse("base:stripe_payment_verify", args=[billing.billing_id])),

    )
    return JsonResponse({"sessionId": checkout_session.id})

def stripe_payment_verify(request, billing_id):
    billing = base_models.Billing.objects.get(billing_id=billing_id)
    session_id = request.GET.get("session_id")

    if not session_id:
        return redirect(f"/payment_status/{billing.billing_id}/?payment_status=failed")
    
    session = stripe.checkout.Session.retrieve(session_id)

    if session.payment_status == "paid":
        if billing.status == "Unpaid":
            billing.status = "Paid"
            billing.save()
            billing.appointment.status = "completed"
            billing.appointment.save()


            doctor_models.Notification.objects.create(
                doctor = billing.appointment.doctor,
                appointment = billing.appointment,
                type = "New Appointment"
            )

            patient_models.Notification.objects.create(
                doctor = billing.appointment.patient,
                appointment = billing.appointment,
                type = "Appointment Scheduled"
            )

            return redirect(f"/payment_status/{billing.billing_id}/?payment_status=paid")
        
        else:
            return redirect(f"/payment_status/{billing.billing_id}/?payment_status=already_paid")
    else:
        return redirect(f"/payment_status/{billing.billing_id}/?payment_status=failed")


def get_paypal_access_toke():
    token_url = "https://api.sandbox.paypal.com/v1/oauth2/token"
    data = { "grant_type": "client_credentials" }
    auth =  (settings.PAYPAL_CLIENT_ID, settings.PAYPAY_SECRET_ID)
    response = requests.post(token_url, data=data, auth=auth)

    if response.status_code == 200:
        print("Access token obtained successfully.")
        response_data = response.json()
        return response_data.get("access_token")
    else:
        raise Exception(f"Failed to obtain access token from PayPal. Status code: {response.status_code}")
    


def paypal_payment_verify(request, billing_id):
    billing = base_models.Billing.objects.get(billing_id=billing_id)
    access_token = get_paypal_access_toke()
    transaction_id = request.GET.get("transaction_id")
    paypal_api_url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{transaction_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {get_paypal_access_toke()}"
    }

    response = requests.get(paypal_api_url, headers=headers)

    if response.status_code == 200:
        paypal_order_data = response.json()
        paypal_payment_status = paypal_order_data['status']

        if paypal_payment_status == "COMPLETED":
            if billing.status == "Unpaid":
                billing.status = "Paid"
                billing.save()
                billing.appointment.status = "completed"
                billing.appointment.save()

                doctor_models.Notification.objects.create(
                    doctor = billing.appointment.doctor,
                    appointment = billing.appointment,
                    type = "New Appointment"
                )

                patient_models.Notification.objects.create(
                    patient = billing.appointment.patient,
                    appointment = billing.appointment,
                    type = "Appointment Scheduled"
                )

                return redirect(f"/payment_status/{billing.billing_id}/?payment_status=paid")
        else:
            return redirect(f"/payment_status/{billing.billing_id}/?payment_status=already_paid")
    else:
        return redirect(f"/payment_status/{billing.billing_id}/?payment_status=failed")

    

@login_required
def payment_status(request, billing_id):
    billing = base_models.Billing.objects.get(billing_id=billing_id)
    payment_status = request.GET.get("payment_status")

    context = {
        "billing":billing,
        "payment_status":payment_status,
    }

    return render(request, "base/payment_status.html", context)

def about(request):
    return render(request, "base/about.html")

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Send email to admin
        try:
            send_mail(
                f"New Contact Form Submission - {subject}",
                f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
                email,
                ['admin@dr-life.com'],
                fail_silently=False,
            )
            
            messages.success(request, "Your message has been sent successfully!")
            return redirect('base:contact')
        except Exception as e:
            messages.error(request, "There was an error sending your message. Please try again later.")
            
    return render(request, "base/contact.html")

def privacy_policy(request):
    return render(request, "base/privacy_policy.html")

def terms_conditions(request):
    return render(request, "base/terms_conditions.html")