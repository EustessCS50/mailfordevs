from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Mail)
admin.site.register(ConfigurationV1)
admin.site.register(SentMailv1)
admin.site.register(SupportTicket)
