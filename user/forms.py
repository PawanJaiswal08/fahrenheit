from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import (PasswordResetForm)
from django.forms import fields
from .models import Profile, UserOTP

# Email Validation On Forget Password
class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError(
                "There is no user registered with the specified email address!")

        return email
    
# Profile Update 
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name','last_name','pic','gender','profession','instagramurl','facebookurl','linkdinurl','bio']
    
class OtpForm(forms.ModelForm):
    class Meta:
        model = UserOTP
        fields = ['otp' , 'user']