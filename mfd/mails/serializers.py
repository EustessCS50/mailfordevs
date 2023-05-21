from email import message
from rest_framework import serializers

from .models import Mail


class MailSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    email = serializers.CharField(max_length=100)
    subject = serializers.CharField(max_length=255)

    class Meta:
        model = Mail
        fields = ["name", "email", "subject", "message"]



# Eustess B