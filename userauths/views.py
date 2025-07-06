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
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            user_type = form.cleaned_data.get("user_type")

            user.first_name = first_name
            user.last_name = last_name
            user.save()

            user = authenticate(request, email=email, password=password)
            login(request, user)

            if user is not None:
                login(request, user)

                print("user ============= ", user)
                dob = form.cleaned_data.get("dob")
                if user_type == "Doctor":
                    doctor_models.Doctor.objects.create(
                        user=user,
                        dob=dob
                    )
                else:
                    patient_models.Patient.objects.create(
                        user=user,
                        dob=dob
                    )

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
    messages.success(request, "Logged Out Successfully")
    return redirect('/')

def forgot_password_view(request):
    if request.method == "POST":
        form = userauths_forms.ForgotPasswordForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            user = userauths_models.User.objects.filter(email=email).first()
            if user is not None:
                # Generate password reset token
                from django.contrib.auth.tokens import default_token_generator
                from django.utils.http import urlsafe_base64_encode
                from django.utils.encoding import force_bytes
                from django.core.mail import send_mail
                from django.template.loader import render_to_string
                from django.conf import settings

                # Generate token and uid
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                # Build reset URL
                reset_url = f"{request.scheme}://{request.get_host()}/reset-password/{uid}/{token}/"
                
                # Prepare email
                email_subject = "Password Reset Request"
                email_body = render_to_string('email/password_reset.html', {
                    'user': user,
                    'reset_url': reset_url,
                })
                
                # Send email
                send_mail(
                    subject=email_subject,
                    message=email_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    html_message=email_body,
                )
                
                messages.success(request, "Password reset instructions have been sent to your email.")
                return redirect('userauths:login')
            else:
                messages.error(request, "No account found with this email address.")
    else:
        form = userauths_forms.ForgotPasswordForm()
    
    context = {"form": form}
    return render(request, "userauths/forgot-password.html", context)


def reset_password_view(request, uidb64, token):
    """
    View to handle the password reset confirmation
    """
    from django.contrib.auth.tokens import default_token_generator
    from django.utils.http import urlsafe_base64_decode
    from django.utils.encoding import force_str
    
    try:
        # Decode the UID and get user
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = userauths_models.User.objects.get(pk=uid)
        
        # Verify token is valid
        if default_token_generator.check_token(user, token):
            if request.method == "POST":
                form = userauths_forms.ResetPasswordForm(request.POST)
                if form.is_valid():
                    password = form.cleaned_data.get("password1")
                    
                    # Set new password
                    user.set_password(password)
                    user.save()
                    
                    messages.success(request, "Your password has been reset successfully. You can now login with your new password.")
                    return redirect('userauths:login')
            else:
                form = userauths_forms.ResetPasswordForm()
                
            context = {"form": form}
            return render(request, "userauths/reset-password.html", context)
        else:
            messages.error(request, "The reset link is invalid or has expired.")
            return redirect('userauths:forgot_password')
    except (TypeError, ValueError, OverflowError, userauths_models.User.DoesNotExist):
        messages.error(request, "The reset link is invalid or has expired.")
        return redirect('userauths:forgot_password')
