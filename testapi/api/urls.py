from django.urls import path
from . import views


urlpatterns = [
    path('v_1.0/', views.getData, name='getData'),
    path('v_1.0/post/', views.postData, name='postData'),
    path('v_1.0/conf/get', views.getConfigurations, name='getconfig'),
    path('v_1.0/dev/get', views.getDevInfo, name='getdev'),
    path('v_1.0/devs', views.getDevs, name='getdevs'),
    path('v_1.0/dev/post', views.createDev, name='createdev'),
]