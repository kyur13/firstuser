from django.contrib import admin
from .models import CustomUser,userotp
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class customuser(UserAdmin):
    model=CustomUser

    list_display=['id','email','username','created_at','updated_at']

@admin.register(userotp)
class useroptadmin(admin.ModelAdmin):
    list_display=['id','email','otp']