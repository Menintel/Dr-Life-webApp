from django.shortcuts import render, redirect
from django.contrib import messages
from userauths import forms as userauths_forms
from django.contrib.auth import authenticate, login, logout
from patient import models as patient_models
from doctor import models as doctor_models
from userauths  import models as userauths_models

# Create your views here.
def register_view(request):
    if request.user.is_authenticated:
        messages.success(request, "You're Logged in")
        return redirect("/")
    
    if request.method == "POST":

        form = userauths_forms.UserRegistrationForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            full_name = form.cleaned_data.get("full_name")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            user_type = form.cleaned_data.get("user_type")

            user = authenticate(request, email=email, password=password)
            login(request, user)

            if user is not None:
                login(request, user)

                print("user ============= ", user)
                if user_type == "Doctor":
                    doctor_models.Doctor.objects.create(user=user, full_name=full_name)
                else:
                    patient_models.Patient.objects.create(user=user, full_name=full_name, email=email)

                messages.success(request, "Account Created successfully")
                return redirect("/")
            else:
                messages.error(request, "Authentication Failed, please Try again.")

    else:
        form = userauths_forms.UserRegistrationForm()
        
    context = {"form":form}

    return render(request, "userauths/sign-up.html", context)

def login_view(request):
    if request.user.is_authenticated:
        messages.success(request, "You're already logged in")
        return redirect("/")
    
    if request.method == "POST":
        form = userauths_forms.LoginForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            
            # Single authentication step
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, "Logged In Successfully")
                next_url = request.GET.get("next", '/')
                return redirect(next_url)
            else:
                messages.error(request, "Invalid email or password")
    else:
        form = userauths_forms.LoginForm()

    context = {"form": form}
    return render(request, "userauths/sign-in.html", context)

def logout_view(request):
    logout(request)
    messages.success(request,  "Logged Out Successfully")

    return redirect("userauths:sign-in")