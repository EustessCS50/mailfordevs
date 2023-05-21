from django.shortcuts import redirect, render
from django.template.loader import render_to_string

from .models import ConfigurationV1


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
    

def sendDMailv2_0():
    from django.core.mail import EmailMultiAlternatives, EmailMessage
    from django.template.loader import render_to_string
    from django.utils.html import strip_tags
    from django.conf import settings
    import os 
    from email.mime.image import MIMEImage

    subject = 'Example Email'
    recipients = ['jitdelivery2022@gmail.com', 'jboyjay29@gmail.com']
    context = {'name': 'Mr B', 'subject':subject, 'message':'Good job'}

    html_message = render_to_string('mailing/receive_mail.html', context)
    plain_message = strip_tags(html_message)

    email = EmailMultiAlternatives(subject, plain_message, from_email=settings.EMAIL_HOST_USER, to=recipients)
    email.attach_alternative(html_message, 'text/html')

    image_path = os.path.join(settings.BASE_DIR, 'myapp', 'static', 'img', 'andy.jpg')
    with open(image_path, 'rb') as f:
        image_data = f.read()
    image = MIMEImage(_imagedata=image_data, _subtype='image/jpeg')
    # image.add_header('content-ID', '<example_image>')
    image.add_header('Content-Disposition', 'inline', filename="myimage")
    email.attach(image)

    email.send()


def sendDMailv2_0_1():
    from django.core.mail import EmailMessage
    from email.mime.image import MIMEImage
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from django.conf import settings
    import os

    subject = 'Example Email v2_0_1'
    recipients = ['jboyjay29@gmail.com', 'jitdelivery2022@gmail.com']
    context = {'name': 'besong'}
    
    html_message = render_to_string('mailing/email2.html', context)

    message = MIMEMultipart()
    message['Subject'] = subject,
    # message['Message'] = html_message
    message['From'] = settings.EMAIL_HOST_USER
    message['To'] = ', '.join(recipients)

    text_message = MIMEText('This is the plain text version of this message.!')
    message.attach(text_message)

    html_message = MIMEText(html_message, _subtype='text/html')
    message.attach(html_message)

    image_path = os.path.join(settings.BASE_DIR, 'myapp', 'static', 'img', 'andy.jpg')
    with open(image_path, 'rb') as f:
        image_data = f.read()

    image = MIMEImage(_imagedata=image_data, _subtype='image/jpeg')
    image.add_header('Content-ID', '<example_image>')
    message.attach(image)

    email = EmailMessage(subject='', body='', from_email=settings.EMAIL_HOST_USER, to=recipients)
    email.attach(message.as_string())
    email.attach_alternative(html_message, _subtype='text/html')
    email.send()


def sendDMailv2():
    from django.core.mail import EmailMessage
    from django.core.mail.backends.smtp import EmailBackend

    from email.mime.image import MIMEImage
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from django.conf import settings
    import os
    

    img_f= os.path.join(settings.BASE_DIR, 'myapp', 'static', 'img', 'andreas.jpg')


    with open(img_f, 'rb') as f:
        img_data = f.read()

    html_part = MIMEMultipart(_subtype='related')

    body = MIMEText('<p>Hello <img src="cid:myimage" /></p>', _charset="utf-8", _subtype='text/html')
    html_part.attach(body)

    img = MIMEImage(img_data,  'image/jpeg')
    # img.add_header('Content-Id', '<myimage>')
    img.add_header('Content-Disposition', 'inline', filename="myimage")
    # img.add_header('content-ID', '<myimage>')

    html_part.attach(img)
    
    msg = EmailMessage('sendDMailv2', html_part, from_email=settings.EMAIL_HOST_USER, to=['jitdelivery2022@gmail.com', 'jboyjay29@gmail.com'])
    msg.attach(html_part)
    msg.fail_silently = False 
    msg.send
    # backend = EmailBackend(
    #     host=config.email_host,
    #     port=config.email_port, 
    #     username=config.email_host_user, 
    #     password=config.email_host_password, 
    #     use_tls=config.email_use_tls, fail_silently=False)

  


def userProfile(request, userId):
    config = ConfigurationV1.objects.get(id=userId)
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        mail_context = {
            'name':name,
            'subject':subject,
            'message':message,
        }
        body = render_to_string('mailing/receive_mail.html', mail_context)

        # sendDMailv1(config=config, subj=subject, bdy=body, to_email=[email])
        sendDMailv2_0_1()
        # sendDMailv2(config=config, subj=subject, from_email=config.email_host_user, to_list=[email])

        return redirect('successM')

    context = {'config':config}
    return render(request, 'profile.html', context)