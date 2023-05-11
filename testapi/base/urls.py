from django.urls import path
from . import views


urlpatterns = [
    path('', views.homePage, name='home'),
    path('account/', views.accounts, name='accounts'),
    path('dev/', views.userProfile, name='dev'),
    path('config/<str:username>/', views.editConfig, name='edit_config'),
    path('contact-us/', views.contact, name='contact'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
]