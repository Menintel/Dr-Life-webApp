from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core import validators
from userauths.models import User
from django.utils import timezone

User = get_user_model()

USER_TYPE = (
    ('Patient', 'Patient'),
    ('Doctor', 'Doctor'),
)

class DateInput(forms.DateInput):
    input_type = 'date'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.attrs.update({
            'class': 'form-control',
            'placeholder': 'Select a date'
        })

    def format_value(self, value):
        if value:
            return value.strftime('%Y-%m-%d')
        return value

#You can even add Icons to the forms if you have any
class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Last Name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'johndoe@gmail.com'}),
                          help_text='Email will be converted to lowercase')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'**********'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'**********'}))
    user_type = forms.ChoiceField(choices=USER_TYPE, widget=forms.Select(attrs={"class":"form-select"}))
    dob = forms.DateField(
        required=True,
        widget=DateInput()
    )

    def clean_email(self):
        return self.cleaned_data.get('email', '').lower()

    class Meta:
        model = User
        fields = ['first_name','last_name','email','password1','password2','user_type', 'dob']


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Email e.g johndoe@gmail.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'**********'}))

    def clean_email(self):
        return self.cleaned_data.get('email', '').lower()

    class Meta:
        model = User
        fields = ['email','password']


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Email e.g johndoe@gmail.com'}))

    def clean_email(self):
        return self.cleaned_data.get('email', '').lower()

    class Meta:
        model = User
        fields = ['email']


class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter new password'})
    )
    password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm new password'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords don't match. Please try again.")
        
        return cleaned_data