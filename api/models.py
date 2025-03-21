from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractUser
from django.utils import timezone
import uuid
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
    email=models.EmailField("email address",unique=True)
    otp=models.IntegerField()