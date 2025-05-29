from django.urls import path
from base import views

app_name = "base"

urlpatterns = [
    path("", views.index, name="index"),
    path("service/<service_id>", views.service_detail, name="service_detail"),
    path("book-appointment/<service_id>/<doctor_id>/", views.book_appointment, name="book_appointment"),
    path("checkout/<billing_id>", views.checkout, name="checkout"),
    
    path("payment_status/<billing_id>/", views.payment_status, name="payment_status"),

    path("stripe_payment/<billing_id>/", views.stripe_payment, name="stripe_payment"),
    path("stripe_payment_verify/<billing_id>", views.stripe_payment_verify, name="stripe_payment_verify"),

    path("paypal_payment_verify/<billing_id>/", views.paypal_payment_verify, name="paypal_payment_verify"),

    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("terms-conditions/", views.terms_conditions, name="terms_conditions"),
    path("services/", views.services, name="services"),
]
