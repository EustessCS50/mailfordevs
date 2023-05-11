from rest_framework import serializers
from base.models import Item, Dev, ConfigurationV1
from django.contrib.auth.models import User



class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    password = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class DevSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    active = serializers.BooleanField(default=True)
    premium = serializers.BooleanField(default=False)
    class Meta:
        model = Dev
        fields = ['user','active', 'premium']


class ConfigurationV1Serializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigurationV1
        fields = ('email_host', 'email_port', 'email_host_user', 'email_host_password', 'email_use_tls', 'email_use_ssl')