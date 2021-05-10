from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from blog.models import Blog , BlogComment
from blog.forms import UpdateForm
from django.shortcuts import get_object_or_404
from blog.templatetags import extras
from django.conf import settings
from django.core.mail import send_mail
import time
from django.http import HttpResponseRedirect
from django.contrib import messages


# Create your views here.

# bloghome
def blogHome(request):
    return render(request , 'blog/blogHome.html')

# categories
def travelling(request):
    blogs= Blog.objects.filter(name="Travel")
    
    context = {
        'blogs': blogs
    }
    return render(request , 'blog/travelling.html' , context)

def technology(request):
    blogs= Blog.objects.filter(name="Technical")
    
    context = {
        'blogs': blogs
    }
    return render(request , 'blog/technology.html' , context)

def dailyLife(request):
    blogs= Blog.objects.filter(name="Daily Life")
    
    context = {
        'blogs': blogs
    }
    return render(request , 'blog/dailylife.html' , context)

def artAndLiterature(request):
    blogs= Blog.objects.filter(name="Art and Literature")
    
    context = {
        'blogs': blogs
    }
    return render(request , 'blog/arts.html' , context)

def sports(request):
    blogs= Blog.objects.filter(name="Sports")
    
    context = {
        'blogs': blogs
    }
    return render(request , 'blog/sports.html' , context)

def education(request):
    blogs= Blog.objects.filter(name="Education")
    
    context = {
        'blogs': blogs
    }
    return render(request , 'blog/education.html' , context)

def entertainment(request):
    blogs= Blog.objects.filter(name="Entertainment")
    
    context = {
        'blogs': blogs
    }
    return render(request , 'blog/entertainment.html' , context)

def food(request):
    blogs= Blog.objects.filter(name="Foody")
    
    context = {
        'blogs': blogs
    }
    return render(request , 'blog/food.html' , context)

def fitness(request):
    blogs= Blog.objects.filter(name="Fitness")
    
    context = {
        'blogs': blogs
    }
    return render(request , 'blog/fitness.html' , context)




@login_required
def new_blog(request):
    if request.method=="POST":
        titleBlog=request.POST['titleBlog']
        name=request.POST['name']
        content =request.POST['content']
        blog=Blog(titleBlog=titleBlog,name=name,content=content,author=request.user)
        messages.success(request, "Blog posted")   
        blog.save()
        return redirect('myblogs')

    return render(request, "blog/newblog.html")

def postview(request , slug):
    blog = Blog.objects.filter(slug=slug).first()
    comments= BlogComment.objects.filter(blog=blog , parent=None)
    replies = BlogComment.objects.filter(blog=blog).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    context={'blog':blog, 'comments': comments, 'user': request.user , 'replyDict': replyDict}
    return render(request , 'blog/postview.html' , context)

@login_required()
def myblogs(request):
    myblogs = Blog.objects.filter(author_id=request.user.id).order_by('-timeStamp')
    context = {'myblogs': myblogs}
    return render(request , 'blog/myblogs.html' ,context)

@login_required()
def blogComment(request,slug):
    if request.method == "POST":
        comment=request.POST.get('comment')
        user=request.user
        blog = Blog.objects.get(slug=slug)
        blogSno =request.POST.get('blogSno')
        parentSno= request.POST.get('parentSno')
        if parentSno=="":
            comment=BlogComment(comment=comment, user=user, blog=blog)
            comment.save()
            messages.success(request, "Comment posted")   
            context={'blog':blog, 'comment': comment, 'user': request.user}
            return redirect(f"/blog/{blog.slug}/" , context)
        else:
            parent= BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment= comment, user=user, blog=blog , parent=parent)
            comment.save()
            messages.success(request, "Reply posted")
            context={'blog':blog, 'comment': comment, 'user': request.user}
            return redirect(f"/blog/{blog.slug}/" , context)
        
    return render(request , 'blog/postview.html')

@login_required
def allblogs(request):
    allblogs= Blog.objects.all()
    context={'allblogs': allblogs}
    return render(request , 'blog/allblogs.html' ,context)

@login_required
def updatepost(request, slug):
    context = {}
    user = request.user
    blog = get_object_or_404(Blog ,slug=slug)
    
    if request.POST:
        form = UpdateForm(request.POST or None, request.FILES or None, instance=blog)
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.save()
            blog = new_blog
            return redirect('/')
    
    
    form = UpdateForm(
        initial={
            "titleBlog" : blog.titleBlog,
            "name": blog.name,
            "content": blog.content,
            "blog": blog,
        }
    )
    
    
    context['form'] = form
    return render(request, 'blog/updatepost.html',context)

@login_required() 
def del_post(request, slug):
    blog = Blog.objects.get(slug=slug)
    blog.delete()
    messages.success(request, "Post Deleted")
    return redirect('/')

@login_required()
def del_comment(request,slug,pk):
    comment = BlogComment.objects.get(pk=pk)
    comment.delete()
    messages.success(request, "Comment Deleted")
    blog = Blog.objects.filter(slug=slug).first()
    comments= BlogComment.objects.filter(blog=blog , parent=None)
    replies = BlogComment.objects.filter(blog=blog).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    context={'blog':blog, 'comments': comments, 'user': request.user , 'replyDict': replyDict}
    return redirect(f"/blog/{blog.slug}/", context)


