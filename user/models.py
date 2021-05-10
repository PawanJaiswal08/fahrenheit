from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    profile_user = models.OneToOneField(User, null=True, related_name="profile" , on_delete=models.CASCADE)
    profile_username = models.TextField(max_length=130,null=True,blank=True)
    first_name = models.TextField(max_length=130,null=True,blank=True)
    last_name = models.TextField(max_length=130,null=True,blank=True)
    pic = models.ImageField(null=True,blank=True)
    gender = models.TextField(max_length=130,null=True,blank=True)
    profession = models.TextField(max_length=130,null=True,blank=True)
    instagramurl = models.TextField(max_length=255,null=True,blank=True)
    facebookurl = models.TextField(max_length=255,null=True,blank=True)
    linkdinurl = models.TextField(max_length=255,null=True,blank=True)
    bio = models.TextField(max_length=255,null=True,blank=True)
    
    def __str__(self):
        return str(self.profile_user)
    
    @property
    def image_url(self):
        if self.pic and hasattr(self.pic, 'url'):
            return self.pic.url


class UserOTP(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	timestamp = models.DateTimeField(auto_now = True)
	otp = models.BigIntegerField()

	def __str__(self):
		return "OTP sent to " + (self.user.username)
    
    
