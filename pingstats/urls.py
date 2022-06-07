from django.contrib import admin
from django.urls import path, include
from . import views

"""
API
"""
from . views import APIReceiver, APIEventReciever

urlpatterns = [
    path('home/', views.home, name='home'),
    path('api/', APIReceiver.as_view(), name='api'),
    path('api/update-status/<int:dev_id>', APIReceiver.as_view()),
    path('api/event/', APIEventReciever.as_view()),
    path('events/', views.event, name='events'),
    path('device-list/', views.listDevices, name='devices'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('about/', views.about, name='about'),
]