from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User

USER_TYPE = {
    ("Patient","Patient"),
    ("Doctor","Doctor"),
}

#You can even add Icons to the forms if you have any
class UserRegistrationForm(UserCreationForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'johndoe@gmail.com'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'**********'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'**********'}))
    user_type = forms.ChoiceField(choices=USER_TYPE, widget=forms.Select(attrs={"class":"form-select"}))

    class Meta:
        model = User
        fields = ['full_name','email','password1','password2','user_type']


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Email e.g johndoe@gmail.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'**********'}))

    class Meta:
        model = User
        fields = ['email','password']