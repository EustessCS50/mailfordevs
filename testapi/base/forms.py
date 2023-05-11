from django import forms
from django.contrib.auth.models import User
from . models import *
from django.contrib.auth.forms import UserCreationForm



#for admin signup
class SignupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email','password']
        widgets = {
        'password': forms.PasswordInput(),
        'email': forms.EmailInput()
        }


#for student related form
class LoginForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class ConfigV1Form(forms.ModelForm):
    class Meta:
        model = ConfigurationV1
        fields = ('email_host', 'email_port', 'email_host_user', 'email_host_password', 'email_use_tls', 'email_use_ssl')
