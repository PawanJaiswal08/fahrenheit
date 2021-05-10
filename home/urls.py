from typing import ValuesView
from django.contrib import admin
from django.urls import path , include , re_path 
from . import views
from django.urls import reverse
from django.conf.urls import url

#
from django_email_verification import urls as mail_urls
# from .forms import EmailValidationOnForgotPassword
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('' , views.home , name='home'),
    path('explore', views.explore , name="explore"),
    path('aboutus', views.aboutus , name="aboutus"),
    path('suggestions', views.writeComplaints , name="writeComplaints"),
    path('developers', views.developers , name="developers"),
    path('allsuggestions', views.allsuggestions , name="allsuggestions"),
    
]