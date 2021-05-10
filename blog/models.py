from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import TextField
from django.urls import reverse
from django.utils.timezone import now
import random
import string 
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.utils.text import slugify

# Create your models here.

def random_string_generator(size = 10, chars = string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance, new_slug = None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.titleBlog)
    Klass = instance.__class__
    max_length = Klass._meta.get_field('slug').max_length
    slug = slug[:max_length]
    qs_exists = Klass.objects.filter(slug = slug).exists()
     
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug = slug[:max_length-5], randstr = random_string_generator(size = 8))
             
        return unique_slug_generator(instance, new_slug = new_slug)
    return slug

class Blog(models.Model):
    sno= models.AutoField(primary_key=True)
    titleBlog= models.CharField(max_length=255)
    author=models.ForeignKey(User, on_delete=models.CASCADE,null=True , related_name="writer")
    name= models.CharField(max_length=255)
    slug=models.SlugField(unique=True,max_length=130,null=True)
    content= TextField(blank=True,null=True)
    timeStamp=models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.titleBlog + " | " + str(self.author)

    def get_absolute_url(self):
        return reverse('blog:post', args=[str(self.slug)])

class BlogComment(models.Model):
    sno= models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    blog=models.ForeignKey(Blog, on_delete=models.CASCADE , related_name ='comments')
    parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True)
    timestamp= models.DateTimeField(default=now)

    def __str__(self):
        return "Comment By" + " " + str(self.user.username) 

@receiver(pre_save, sender=Blog)
def pre_save_receiver(sender, instance, *args, **kwargs):
   if not instance.slug:
       instance.slug = unique_slug_generator(instance)
