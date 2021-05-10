from django.shortcuts import render , HttpResponse , redirect
from home.models import Complaint
from django.contrib import messages


# Create your views here.

def home(request):
    return render(request , 'home/home.html')

def explore(request):
    return render(request , 'home/explore.html')

def aboutus(request):
    return render(request , 'home/aboutus.html')

def developers(request):
    return render(request , 'home/meet_developers.html')

def writeComplaints(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content =request.POST['content']
        complaint=Complaint(name=name, email=email, phone=phone, content=content)
        complaint.save()
        messages.info(request,'Your suggestion has been sent successfully!')
        return redirect('/')
    return render(request, "home/suggestions.html")

def allsuggestions(request): 
    allComplaints= Complaint.objects.all()
    context={'allComplaints': allComplaints}
    return render(request, "home/allsuggestions.html", context)
