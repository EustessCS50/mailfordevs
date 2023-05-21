from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import ValidationError

from . models import User
from mails.models import Mail


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=80)
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def validate(self, attrs):

        username_exists = User.objects.filter(username=attrs["username"]).exists()

        if username_exists:
            raise ValidationError("Username has already been used")

        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = super().create(validated_data)

        user.set_password(password)

        user.save()

        Token.objects.create(user=user)

        return user
    

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["username", "password"]

    def validate(self, attrs):

        username_exists = User.objects.filter(username=attrs["username"]).exists()

        if username_exists == False:
            raise ValidationError("User does not exist!")

        return super().validate(attrs)


class CurrentUserMailsSerializer(serializers.ModelSerializer):
    mails = serializers.HyperlinkedRelatedField(
        many=True, view_name="mail_detail", queryset=User.objects.all()
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "mails"]


class MailSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    email = serializers.CharField(max_length=100)
    subject = serializers.CharField(max_length=255)

    class Meta:
        model = Mail
        fields = ["name", "email", "subject", "message"]





# Eustess B