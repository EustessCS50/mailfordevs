from django.shortcuts import render, redirect

from accounts.tokens import create_jwt_pair_for_user
from .utils import count_mails


from .forms import *

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token

from . models import *

# Create your views here.


##############################

from django.conf import settings
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage as EM
from django.template.loader import render_to_string


from .forms import *
from . models import *
from .dynamics import sendDMailv1

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token


# Create your views here.
@login_required(login_url='login')
def homePage(request):
    user = request.user
    jwt = create_jwt_pair_for_user(user)
    auth_token = request.user.auth_token
    config = ConfigurationV1.objects.filter(dev=user)
    mails = Mail.objects.filter(dev=user)
    no_mails = count_mails(user)
    context = {'config': config, 'mails':mails, 'no_mails':no_mails, 'jwt':jwt, 'auth_token':auth_token}
    return render(request, 'index.html', context)

@login_required(login_url="login")
def user_mails(request):
    user = request.user
    mails = Mail.objects.filter(dev=user)
    no_mails = count_mails(user)
    context = {'mails':mails, 'no_mails':no_mails}
    return render(request, 'user-mails.html', context)

@login_required(login_url="login")
def mail_detail(request, pk):
    mail = Mail.objects.get(id=pk)
    context = {'mail':mail}
    return render(request, 'mail_detail.html', context)

@login_required(login_url="login")
def reply_mail(request, pk):
    form = SendOrReplyFormv1()
    user = request.user
    reply_email = Mail.objects.get(id=pk)
    to_email = reply_email.email
    from_email = request.user.email
    config = ConfigurationV1.objects.get(dev=user)
    if request.method == "POST":
        form = SendOrReplyFormv1(request.POST)
        if form.is_valid():
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')
            form2 = form.save(False)
            form2.dev = user
            form2.email = to_email
            form2.save()
            if form2.save():
                body = render_to_string('mailing/replymail_template.html', context={'subject':subject,'message':message})
                sendDMailv1(config=config, subj=subject, bdy=body, to_email=[to_email, from_email])
    context = {'supportForm':form, "to_email":to_email, 'from_email':from_email}
    return render(request, 'replymail.html', context)

@login_required(login_url='login')
def testmail(request):
    form = EmailFormv1()
    user = request.user
    config = ConfigurationV1.objects.get(user=user)
    if request.method == "POST":
        form = EmailFormv1(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')
            form.save()
            if form.save():
                body = render_to_string('mailing/mail_template.html', context={'name':name,'email':email,'subject':subject,'message':message})
                sendDMailv1(config=config, subj=subject, bdy=body, to=[email])
    context = {'supportForm':form}
    return render(request, 'testmail.html', context)


@login_required(login_url='login')
def userProfile(request):
    user = request.user
    token = request.user.auth_token
    print("Token: ", token)
    config = ConfigurationV1.objects.get(user=user)

    context={'user':user, 'dev':user, 'config':config}
    return render(request, 'profile.html', context)


@login_required(login_url="login")
def viewUpdateConfig(request, username):
    user = request.user
    config = ConfigurationV1.objects.get(dev=user)
    config_form = ConfigV1Form(instance=config)
    if request.method == "POST":
        config_form = ConfigV1Form(request.POST, instance=config)
        if config_form.is_valid():
            config_form.save()
            return redirect('home')
    
    context={'configForm':config_form}
    return render(request, 'edit_config.html', context)


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        userform = SignupForm()
        if request.method == "POST":

            userform = SignupForm(request.POST)

            if userform.is_valid():
                user = userform.save()
                if userform.save():
                    authtoken = Token.objects.create(user=user)
                    jwt = create_jwt_pair_for_user(user)
                    ConfigurationV1.objects.create(dev=user)
                    Mail.objects.create(
                        dev=user,
                        name="EusTech",
                        email="info@eustech.com",
                        subject="Sample Mail",
                        message="This is where mails sent to you from your website/app/software is been displayed. You can also see these mails from your mailing host: e.g Gmail."
                    )
                    SentMailv1.objects.create(
                        dev=user,
                        email="info@eustech.com",
                        subject='Sample Reply',
                        message="This is where mails you reply from your website/app/software is been displayed. You can also see these mails from your mailing host: e.g Gmail."
                    )

                    name = user.username
                    email = user.email 
                    admin_email = settings.EMAIL_HOST_USER

                    body = render_to_string('mailing/reg_mail.html', context={'name':name})

                    mailer = EM(
                        subject="Account Creation", 
                        body=body,
                        from_email=settings.EMAIL_HOST_USER,
                        to=[email, settings.EMAIL_HOST_USER],
                        )
                    mailer.fail_silently = True
                    mailer.send()
                    login(request=request, user=user)
                    return redirect('home')

        context = {'userForm': userform}
        return render(request, 'signup.html', context)

def docs(request):
    return render(request, 'docs.html')


def accounts(request):
    return render(request, 'accounts.html')

def contact(request):
    supportform = SupportTicketForm()
    if request.method == "POST":
        supportform = SupportTicketForm(request.POST)
        if supportform.is_valid:
            supportform.save()
        
    context = {'supportForm': supportform}
    return render(request, 'contact.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request=request, username=username, password=password)

        if user is None:
            print('User does not exist')
            return redirect('login')
        else:
            login(request=request, user=user)
            jwt = create_jwt_pair_for_user(user)
            return redirect('home')
    context = {}
    return render(request, 'login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')

