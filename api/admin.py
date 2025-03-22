from django.contrib import admin
from .models import CustomUser,userotp,userimage
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class customuser(UserAdmin):
    model=CustomUser

    list_display=['id','email','username','created_at','updated_at']

@admin.register(userotp)
class useroptadmin(admin.ModelAdmin):
    list_display=['id','email','otp','created_at','expiration_time']


@admin.register(userimage)
class userimgadmin(admin.ModelAdmin):
    list_display=['id','created_by','img1','img2','img3','created_at','updated_at','background']