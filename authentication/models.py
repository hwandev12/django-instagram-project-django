from django.db import models
from django.contrib.auth.models import User
import PIL 
from PIL import Image
from django.urls import reverse
from django.db.models.signals import post_save
import uuid
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', unique=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_picture", null=True, default="default.jpg")
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    url = models.URLField(max_length=200, null=True, blank=True)

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username} - Profile"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.width > 300 and img.height > 300:
            general_size = (300, 300)
            img.thumbnail(general_size)
            img.save(self.image.path)    

def create_user_profile(instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
def save_user_profile(instance, **kwargs):
    instance.profile.save()
    
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
    