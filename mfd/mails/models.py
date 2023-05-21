from pickle import TRUE

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db import models

# Create your models here.

User = get_user_model()


class ConfigurationV1(models.Model):
    dev = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    email_host = models.CharField(_(u'EMAIL_HOST'), max_length=1024, default=None, null=True)
    email_port = models.PositiveSmallIntegerField(_(u'EMAIL_PORT'), default=587)
    email_host_user = models.CharField(_(u'EMAIL_HOST_USER'), max_length=255, default=None, null=True)
    email_host_password = models.CharField(_(u'EMAIL_HOST_PASSWORD'), max_length=255, default=None, null=True)
    email_use_tls = models.BooleanField(_(u'EMAIL_USE_TLS'), default=True, null=True)
    email_use_ssl = models.BooleanField(_(u'EMAIL_USE_SSL'), default=False, null=True)

    def __str__(self):
        return f'{self.dev}--{self.email_host_user}'
    

class Mail(models.Model):
    dev = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    subject = models.CharField(max_length=1024, null=True, blank=True)
    message = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True) 
    attachment = models.FileField(null=True, blank=True, default=None)

 

    def __str__(self):
        return f"{self.subject} by {(self.name)}"

    class Meta:
        ordering = ["-created"]

class SentMailv1(models.Model):
    dev = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    subject = models.CharField(max_length=1024, null=True, blank=True)
    message = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True) 
    attachment = models.FileField(null=True, blank=True, default=None)

 

    def __str__(self):
        return f"{self.subject} to {(self.email)}"

    class Meta:
        ordering = ["-created"]



class SupportTicket(models.Model):
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=50)
    subject = models.CharField(max_length=100, null=True)
    message = models.TextField(null=True)

    def __str__(self):
        return f"{self.subject} by {self.name}"

#     logo = models.ImageField(null=True, blank=True, default=None)
#     attachment1 = models.FileField(null=True, blank=True, default=None)
#     attachment2 = models.FileField(null=True, blank=True, default=None)
#     added = models.DateTimeField(auto_now_add=True)
