from typing import ValuesView
from django.contrib import admin
from django.urls import path
from . import views
from .forms import EmailValidationOnForgotPassword
from django.contrib.auth import views as auth_views


urlpatterns = [
    
    path('signin' , views.signin , name="signin"),
    
    # MOBILE PATHS
    path('msignup', views.mobilesignup , name="mobilesignup"),
    path('msignin' , views.mobilesignin , name="mobilesignin"),
    
    # HANDLE SIGNUP AND SIGNIN IN PC 
    path('signup', views.handleSignUp , name="handleSignUp"),
    path('login', views.handleLogin , name="handleLogin"),
    path('logout', views.handleLogout , name="handlelogout"),
    
    path('resendOTP', views.resend_otp , name="resend_otp"),
    path("password-reset", auth_views.PasswordResetView.as_view(template_name="user/password_reset.html",form_class=EmailValidationOnForgotPassword), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="user/password_reset_done.html"), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view(template_name="user/password_reset_confirm.html"), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name="user/password_reset_complete.html"), name="password_reset_complete"),
    path('profile/<str:profile_username>/', views.profile , name="profile"),
    path('updateprofile/<str:profile_username>', views.updateprofile , name="updateprofile"),
]
