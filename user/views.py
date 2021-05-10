from django.http import request
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User 
from django.contrib.auth  import authenticate,  login, logout
from django.contrib.auth.decorators import login_required
import os
import random
from django.conf import settings
from django.core.mail import send_mail
from .models import Profile, UserOTP 
from .forms import ProfileUpdateForm , OtpForm
from blog.models import Blog
from django.contrib import messages
from django.http import HttpResponseRedirect
import re


# Create your views here.

def signin(request):
    if request.user_agent.is_mobile:
        is_mobile = True
    else:
        is_mobile = False
        
    # print(request.user_agent.is_mobile)
    context={
        'is_mobile': is_mobile
    }
    return render(request , 'user/signin.html' , context)

def mobilesignup(request):
    return render(request , 'user/signup_mobile.html')

def mobilesignin(request):
    return render(request , 'user/signin.html')

def handleSignUp(request):
    if request.method=="POST":
        user_otp = request.POST.get('otp')
        if user_otp:
            get_user_username = request.POST.get('username')
            user = User.objects.get(username=get_user_username)
            if int(user_otp) == UserOTP.objects.filter(user = user).last().otp:
                user.is_active = True
                user.save()
                profile_user = Profile(profile_user = user)
                profile_user.save()
                messages.success(request,"Account Successfully Created !")
                return redirect('signin')
            else:
                messages.error(request,"Wrong OTP entered ! Try Again")
                return render(request , 'user/checkOtp.html', {'myuser': user})
            
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        if not username.isalnum():
            messages.error(request, " Username should only contain letters and numbers")
            return redirect('signin')
        
        flag = 0
        while True:  
            if (len(pass1)<8):
                flag = -1
                break
            elif not re.search("[a-z]", pass1):
                flag = -1
                break
            elif not re.search("[A-Z]", pass1):
                flag = -1
                break
            elif not re.search("[0-9]", pass1):
                flag = -1
                break
            elif not re.search("[_@$]", pass1):
                flag = -1
                break
            elif re.search("\s", pass1):
                flag = -1
                break
            else:
                flag = 0
                break
        
        if flag ==-1:
            print("Not a Valid Password")
            messages.error(request, "Use strong passwords consist of a combination of uppercase and lowercase letters, numbers and special symbols [_@$]")
            return redirect('signin')
        
        if (pass1!= pass2):
            messages.error(request, " Passwords do not match , Try again ")
            return redirect('signin')

        # Create the user
        myuser = User.objects.create_user(username,email,pass1, is_active = False)
        myuser.username = username
        myuser.user_email = email
        myuser.save()
        myuser_otp = random.randint(100000, 999999)
        UserOTP.objects.create(user = myuser, otp = myuser_otp)
        mess = f"Hello {myuser.username},\nYour OTP is { myuser_otp }\nThanks!"
        send_mail(
            "Welcome to Fahrenheit - Verify Your Email",
            mess,
            settings.EMAIL_HOST_USER,
            [myuser.email],
            fail_silently = False
        )

        context = {'myuser': myuser , 'emailOtp': myuser_otp }
        messages.info(request, "OTP is Sent to your email !")
        return render(request , 'user/checkOtp.html' , context)

    else:
        return render(request , 'user/signin.html')
        
def handleLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user = authenticate(username = loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            # messages.success(request, "Successfully Logged In")
            if request.POST.get('next'):
                # print(request.POST.get('next'))
                return redirect(request.POST.get('next'))
            messages.success(request,"Login Successful")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect('signin')

    return render(request , 'user/signin.html')

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')

def resend_otp(request):
    if request.method == "GET":
        get_user = request.GET['user']
        if User.objects.filter(username = get_user).exists() and not User.objects.get(username = get_user).is_active:
            myuser = User.objects.get(username=get_user)
            myuser_otp = random.randint(100000, 999999)
            UserOTP.objects.create(user = myuser, otp = myuser_otp)
            mess = f"Hello {myuser.username},\nYour OTP is { myuser_otp }\nThanks!"
            send_mail(
                "Welcome to Fahrenheit - Verify Your Email",
                mess,
                settings.EMAIL_HOST_USER,
                [myuser.email],
                fail_silently = False
            )
            return HttpResponse("Resend")
    return HttpResponse("Can't Send ")

def profile(request,profile_username):
    
    try:
        profile_user = User.objects.get(username=profile_username)
        blogs = Blog.objects.filter(author_id=profile_user.id)
    except:
        raise HttpResponse("Error")
    
    # print(profile_user)
    # print(blogs)
    profileusername = profile_user.username.capitalize()
    gender = profile_user.profile.gender
    pic = profile_user.profile.pic
    bio = profile_user.profile.bio
    
    context = {
        'profileusername':profileusername,
        'profile_user' : profile_user,
        'gender' : gender,
        'pic' : pic,
        'blogs':blogs,
        'bio':bio,
    }
    return render(request , 'user/profile.html',context)

@login_required
def updateprofile(request ,profile_username):
    if request.POST:
        old_image = ""
        if request.user.profile.pic:
            old_image = request.user.profile.pic.path
        update_form = ProfileUpdateForm(request.POST or None, request.FILES or None,instance=request.user.profile)
        print(profile_username)
        if update_form.is_valid():
            print(request.user.username)
            if os.path.exists(old_image):
                os.remove(old_image)
            update_form.save()
            return redirect(f'/user/profile/{request.user.username}/')

    else:
        update_form = ProfileUpdateForm(instance=request.user)
        
        
    form = ProfileUpdateForm(
        initial={
            "first_name" : request.user.profile.first_name,
            "last_name" : request.user.profile.last_name,
            "gender" : request.user.profile.gender,
            "profession" : request.user.profile.profession,
            "instagramurl" : request.user.profile.instagramurl,
            "facebookurl" : request.user.profile.facebookurl,
            "linkdinurl" : request.user.profile.linkdinurl,
            "bio" : request.user.profile.bio,
        }
    )
    
    totalblogs = Blog.objects.filter(author_id=request.user.id).count()

    context={
        'update_form':update_form,
        'form':form,
        'totalblogs':totalblogs,
    }
    return render(request, 'user/updateprofile.html',context)
  

