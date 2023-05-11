from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# Create your models here.


class Item(models.Model):
    name = models.CharField(max_length=255, null=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'
    
class Dev(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    premium = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}'

class ConfigurationV1(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    email_host = models.CharField(_(u'EMAIL_HOST'), max_length=1024, default=None, null=True)
    email_port = models.PositiveSmallIntegerField(_(u'EMAIL_PORT'), default=587)
    email_host_user = models.CharField(_(u'EMAIL_HOST_USER'), max_length=255, default=None, null=True)
    email_host_password = models.CharField(_(u'EMAIL_HOST_PASSWORD'), max_length=255, default=None, null=True)
    email_use_tls = models.BooleanField(_(u'EMAIL_USE_TLS'), default=True, null=True)
    email_use_ssl = models.BooleanField(_(u'EMAIL_USE_SSL'), default=False, null=True)

    def __str__(self):
        return f'{self.user}--{self.email_host_user}'
    

class Email(models.Model):
    pass
    


