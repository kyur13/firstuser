from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractUser
from django.utils import timezone
import uuid
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
import json
from django.conf import settings
import os
class customusermanager(BaseUserManager):
    def _create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError("email must have..")
        email=self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self,email,password,**extra_fields):
        extra_fields.setdefault('is_active',False)
        return self._create_user(email,password,**extra_fields)
    
    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',True)
        return self._create_user(email,password,**extra_fields)

class CustomUser(AbstractUser):
    USERNAME_FIELD=None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email=models.EmailField("email address",unique=True)
    username=models.CharField(max_length=100,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    objects=customusermanager()


class userotp(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    otp=models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    expiration_time = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.expiration_time = self.created_at + timedelta(minutes=1)
        super(userotp, self).save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expiration_time

class userimage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    img1=models.ImageField(upload_to='uuid',blank=True,null=True,max_length=500)
    img2=models.ImageField(upload_to='uuid',blank=True,null=True,max_length=500)
    img3=models.ImageField(upload_to='uuid',blank=True,null=True,max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    background=models.CharField(max_length=150)

@receiver(post_save, sender=userimage)
def create_status_json(sender, instance, created, **kwargs):
    if created:  
        user_uuid = instance.created_by.id 
        tmp_dir = os.path.join(settings.MEDIA_ROOT, 'tmp', str(user_uuid))
                
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
        
        status_file_path = os.path.join(tmp_dir, 'status.json')
        
        status_data = {'progress': 0, 'message': 'processing started'}

        with open(status_file_path, 'w') as json_file:
            json.dump(status_data, json_file)