from django import forms
from django.contrib.auth.models import User
from . models import *
from django.contrib.auth.forms import UserCreationForm



#for admin signup
class SignupForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1', 'password2']
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

class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = "__all__"

class EmailFormv1(forms.ModelForm):
    class Meta:
        model = Mail
        fields = ('name', 'email', 'subject', 'message')

class SendOrReplyFormv1(forms.ModelForm):
    class Meta:
        model = SentMailv1
        fields = ('email', 'subject', 'message')
