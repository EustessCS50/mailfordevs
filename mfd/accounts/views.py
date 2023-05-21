import imp
from os import error
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import logout
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from mails.dynamics import sendDMailv1

from mails.models import ConfigurationV1

from .serializers import SignUpSerializer, LoginSerializer, MailSerializer
from .tokens import create_jwt_pair_for_user
from django.template.loader import render_to_string

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
# from rest_framework.authtoken.models import Token


# Create your views here.


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = []

    def post(self, request: Request):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            response = {"message": "User Created Successfully", "data": serializer.data}

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = []

    def post(self, request: Request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:

            tokens = create_jwt_pair_for_user(user)

            response = {"message": "Login Successfull", "tokens": tokens}
            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response(data={"message": "Invalid username or password"})

    def get(self, request: Request):
        content = {"user": str(request.user), "auth": str(request.auth)}

        return Response(data=content, status=status.HTTP_200_OK)
    
@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def mail_v1(request):
    user = request.user
    config = ConfigurationV1.objects.get(dev=user)
    serializer = MailSerializer()
    if request.method == "POST":
        serializer = MailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(dev=user)
            name = serializer.data.get('name')
            email = serializer.data.get('email')
            subject = serializer.data.get('subject')
            message = serializer.data.get('message')
            body = render_to_string('mail_template.html', context={'name':name,'email':email,'subject':subject,'message':message})
            sendDMailv1(config=config, subj=subject, bdy=body, to_email=[email, config.email_host_user])

        content = {"message":"Mail was successfullty sent.", "data":serializer.data}
        return Response(content, status=status.HTTP_201_CREATED)
    else:
        content={"message":"Read the documentation for this endpoint!."}
        return Response(content, status=status.HTTP_204_NO_CONTENT)


def logout_view(request):
    logout(request)
    Response(content={"message":"Logged Out Successfully"}, status=status.HTTP_200_OK)



# Eustess B