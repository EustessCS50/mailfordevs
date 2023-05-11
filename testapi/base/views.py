from django.shortcuts import render, redirect


from .forms import *

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token

from . models import *

# Create your views here.

def homePage(request):
    context = {}
    return render(request, 'index.html', context)


@login_required(login_url='login')
def userProfile(request):
    user = request.user
    dev = Dev.objects.get(user=user)
    token = dev.user.auth_token
    print("Token: ", token)
    config = ConfigurationV1.objects.get(user=user)

    context={'user':user, 'dev':dev, 'config':config}
    return render(request, 'profile.html', context)

def editConfig(request, username):
    user = request.user
    config = ConfigurationV1.objects.get(user=user)
    config_form = ConfigV1Form(instance=config)
    if request.method == "POST":
        config_form = ConfigV1Form(request.POST, instance=config)
        if config_form.is_valid():
            config_form.save()
            return redirect('dev')
    
    context={'config_form':config_form}
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
                    Dev.objects.create(user=user)
                    Token.objects.create(user=user)
                    ConfigurationV1.objects.create(user=user)

                    login(request=request, user=user)
                    return redirect('home')

        context = {'userForm': userform}
        return render(request, 'signup.html', context)



def accounts(request):
    return render(request, 'accounts.html')
def contact(request):
    return render(request, 'contact.html')

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
            return redirect('home')
    context = {}
    return render(request, 'login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')



# @login_required(login_url='login')
# def profilePage(request):
#     student = request.user
#     if request.method == "POST":
#         form = UserForm(request.POST, instance=student)
#         profile_form = StudentForm(request.POST, request.FILES, instance=request.user.profile)
#         if form.is_valid() and profile_form.is_valid():
#             user_form = form.save()
#             custom_form = profile_form.save(False)
#             custom_form.user = user_form
#             custom_form.save()
#             return redirect('home')
#     else:
#         form = UserForm(instance=student)
#         profile_form = StudentForm(instance=request.user.profile)

#     context = {'form': form, 'profile_form': profile_form}
#     return render(request, 'profile.html', context)