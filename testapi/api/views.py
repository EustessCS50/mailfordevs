from rest_framework.response import Response
from django.contrib.auth.models import User

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.authtoken.models import Token

from .serializers import *
from base.models import *


# for user in User.objects.all():
#         Token.objects.create(user=user)    

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def getData(request):
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    
    content = {
        'user': str(request.user),
        'auth': str(request.user.auth_token),
        'item': serializer.data
    }
    
    return Response(content, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getConfigurations(request):
    auth_token = None
    dev = request.user.dev
    user = request.user
    config = ConfigurationV1.objects.get(user=dev)
    print(config)
    serializer = ConfigurationV1Serializer(config, many=False)
    print(dev)
    content={'user':str(request.user),'auth': str(request.user.auth_token),'config':serializer.data}
    # print(dev)
    return Response(content)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getDevInfo(request):
    dev = request.user.dev
    user = request.user
    serializer = DevSerializer(dev, many=False)
    print(dev)
    content={'user':str(request.user),'auth': str(request.user.auth_token),'dev':serializer.data}
    # print(dev)
    return Response(content)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def getDevs(request):
    devs = Dev.objects.all() 
    user = request.user
    serializer = DevSerializer(devs, many=True)
    content={'admin':str(request.user),'auth': str(request.user.auth_token),'devs':serializer.data}
    # print(dev)
    return Response(content)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def postData(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createDev(request):
    serializer = DevSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        if serializer.save():
            user = serializer.user
            Token.objects.create(user=user)
    content = {'message':'Dev created Successfully', 'data':serializer.data}
    return Response(content, status="HTTP_201_OK")

def sendDMailv1(config:object, subj:str, bdy, to_email:list):
    from django.core.mail import EmailMessage
    from django.core.mail.backends.smtp import EmailBackend

    backend = EmailBackend(
        host=config.email_host, 
        port=config.email_port, 
        username=config.email_host_user, 
        password=config.email_host_password, 
        use_tls=config.email_use_tls, fail_silently=True)
    
    emailSender = EmailMessage(
        subject=subj, 
        body=bdy, 
        from_email=config.email_host_user, 
        to=to_email, 
        connection=backend)
    emailSender.send()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sendMailV1(request):
    # sendDMailv1(config:object, subj:str, bdy, to_email:list)
    return Response(request)



# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm

# from django.template.loader import render_to_string

# from django.contrib.auth.models import User
# from . models import Configuration

# # Create your views here.

# def home(request):
#     users = User.objects.all()
#     context = {'users':users}
#     return render(request, 'index.html', context)
    

# def sendDMailv2_0():
#     from django.core.mail import EmailMultiAlternatives, EmailMessage
#     from django.template.loader import render_to_string
#     from django.utils.html import strip_tags
#     from django.conf import settings
#     import os 
#     from email.mime.image import MIMEImage

#     subject = 'Example Email'
#     recipients = ['jitdelivery2022@gmail.com', 'jboyjay29@gmail.com']
#     context = {'name': 'Mr B', 'subject':subject, 'message':'Good job'}

#     html_message = render_to_string('mailing/receive_mail.html', context)
#     plain_message = strip_tags(html_message)

#     email = EmailMultiAlternatives(subject, plain_message, from_email=settings.EMAIL_HOST_USER, to=recipients)
#     email.attach_alternative(html_message, 'text/html')

#     image_path = os.path.join(settings.BASE_DIR, 'myapp', 'static', 'img', 'andy.jpg')
#     with open(image_path, 'rb') as f:
#         image_data = f.read()
#     image = MIMEImage(_imagedata=image_data, _subtype='image/jpeg')
#     # image.add_header('content-ID', '<example_image>')
#     image.add_header('Content-Disposition', 'inline', filename="myimage")
#     email.attach(image)

#     email.send()


# def sendDMailv2_0_1():
#     from django.core.mail import EmailMessage
#     from email.mime.image import MIMEImage
#     from email.mime.multipart import MIMEMultipart
#     from email.mime.text import MIMEText
#     from django.conf import settings
#     import os

#     subject = 'Example Email v2_0_1'
#     recipients = ['jboyjay29@gmail.com', 'jitdelivery2022@gmail.com']
#     context = {'name': 'besong'}
    
#     html_message = render_to_string('mailing/email2.html', context)

#     message = MIMEMultipart()
#     message['Subject'] = subject,
#     # message['Message'] = html_message
#     message['From'] = settings.EMAIL_HOST_USER
#     message['To'] = ', '.join(recipients)

#     text_message = MIMEText('This is the plain text version of this message.!')
#     message.attach(text_message)

#     html_message = MIMEText(html_message, _subtype='text/html')
#     message.attach(html_message)

#     image_path = os.path.join(settings.BASE_DIR, 'myapp', 'static', 'img', 'andy.jpg')
#     with open(image_path, 'rb') as f:
#         image_data = f.read()

#     image = MIMEImage(_imagedata=image_data, _subtype='image/jpeg')
#     image.add_header('Content-ID', '<example_image>')
#     message.attach(image)

#     email = EmailMessage(subject='', body='', from_email=settings.EMAIL_HOST_USER, to=recipients)
#     email.attach(message.as_string())
#     email.attach_alternative(html_message, _subtype='text/html')
#     email.send()


# def sendDMailv2():
#     from django.core.mail import EmailMessage
#     from django.core.mail.backends.smtp import EmailBackend

#     from email.mime.image import MIMEImage
#     from email.mime.multipart import MIMEMultipart
#     from email.mime.text import MIMEText
#     from django.conf import settings
#     import os
    

#     img_f= os.path.join(settings.BASE_DIR, 'myapp', 'static', 'img', 'andreas.jpg')


#     with open(img_f, 'rb') as f:
#         img_data = f.read()

#     html_part = MIMEMultipart(_subtype='related')

#     body = MIMEText('<p>Hello <img src="cid:myimage" /></p>', _subtype='text/html')
#     html_part.attach(body)

#     img = MIMEImage(img_data,  'image/jpeg')
#     # img.add_header('Content-Id', '<myimage>')
#     img.add_header('Content-Disposition', 'inline', filename="myimage")
#     # img.add_header('content-ID', '<myimage>')

#     html_part.attach(img)
    
#     msg = EmailMessage('sendDMailv2', html_part, from_email=settings.EMAIL_HOST_USER, to=['jitdelivery2022@gmail.com', 'jboyjay29@gmail.com'])
#     msg.attach(html_part)
#     msg.fail_silently = False 
#     msg.send
#     # backend = EmailBackend(
#     #     host=config.email_host, ~~~
#     #     port=config.email_port, 
#     #     username=config.email_host_user, 
#     #     password=config.email_host_password, 
#     #     use_tls=config.email_use_tls, fail_silently=False)

  


# def userProfile(request, userId):
#     config = Configuration.objects.get(id=userId)
#     if request.method == "POST":
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         subject = request.POST.get('subject')
#         message = request.POST.get('message')

#         mail_context = {
#             'name':name,
#             'subject':subject,
#             'message':message,
#         }
#         body = render_to_string('mailing/receive_mail.html', mail_context)

#         # sendDMailv1(config=config, subj=subject, bdy=body, to_email=[email])
#         sendDMailv2_0_1()
#         # sendDMailv2(config=config, subj=subject, from_email=config.email_host_user, to_list=[email])

#         return redirect('successM')