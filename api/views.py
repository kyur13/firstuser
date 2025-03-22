from django.shortcuts import render
from .models import CustomUser,userotp,userimage
from .serializer import customuserserializer,userimgserilizer
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status 
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
import random
from rest_framework import generics
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
import os

class register(generics.CreateAPIView):
    queryset=CustomUser.objects.all()
    serializer_class=customuserserializer
    def create(self, request, *args, **kwargs):
        mail=request.data.get('email')
        if CustomUser.objects.filter(email=mail).exists():
            user=CustomUser.objects.get(email=mail)
            if user.is_active is False:
                otp=random.randint(100000,999999)
                subject="Opt from lnxct"
                message="your registration otp is "+str(otp)
                send_mail(
                    subject,
                    message,
                    "dummyworkingco@gmail.com", 
                    [mail],     
                    fail_silently=False,
                )
                if userotp.objects.filter(email=user).exists():
                    change=userotp.objects.get(email=user)
                    change.otp=otp
                    change.created_at = timezone.now()
                    change.expiration_time = timezone.now() + timedelta(minutes=1)
                    change.save()
                else:
                    userotp.objects.create(email=user,otp=otp)
                return Response({'message': 'OTP sent again to your email. Please verify.', 'success': True})
            else:
                return Response({'message':'user is already register','success':False})
        otp=random.randint(100000,999999)
        subject="Opt from lnxct"
        message="your registration otp is "+str(otp)
        send_mail(
            subject,
            message,
            "dummyworkingco@gmail.com", 
            [mail],     
            fail_silently=False,
        )
        
        serial=customuserserializer(data=request.data)
        if serial.is_valid():
            password = serial.validated_data.get('password')
            serial.validated_data['password']=make_password(password)
            serial.validated_data['username']=mail.split('@')[0]
            serial.validated_data['is_active']=False
            serial.save()
            
            user = CustomUser.objects.get(email=mail)
            if userotp.objects.filter(email=user).exists():
                change=userotp.objects.get(email=user)
                change.otp=otp
                change.save()
            else:
                userotp.objects.create(email=user,otp=otp)
            return Response({'message':'user register successfully..','success':True})
        return Response({'message':'user not register','success':False})

class verify(generics.GenericAPIView):
    def post(self,request):
        mail=request.data.get('email')
        otpreq=request.data.get('otp')
        try:
            user = CustomUser.objects.get(email=mail)
            change=userotp.objects.get(email=user,otp=otpreq)
        except (CustomUser.DoesNotExist, userotp.DoesNotExist):
            return Response({'message': 'Invalid email or OTP', 'success': False})
       
        
        if change.expiration_time < timezone.now():
            return Response({'message':'otp is expire please regenrate','success':False})
        if change:
            change=CustomUser.objects.get(email=mail)
            change.is_active=True
            change.save()
            return Response({'message':'user verify successfully..','success':True})
        else:
            return Response({'message':'Invalid otp','success':False})

class login(generics.GenericAPIView):
    def post(self,request):
        mail=request.data.get('email')
        psw=request.data.get('password')
        
        user=authenticate(email=mail,password=psw)

        if user is not None:
            refresh=RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                'message': 'Login successful',
                'refresh_token':str(refresh),
                'access_token': access_token,
                'success':True
            }, status=status.HTTP_200_OK)
        
        return Response({
                'message': 'Invalid credentials',
                'success':False
            }, status=status.HTTP_200_OK)
    
class forgotepsw(generics.GenericAPIView):
    def post(self,request):
        mail=request.data.get('email')
        if CustomUser.objects.filter(email=mail).exists():
            user = CustomUser.objects.get(email=mail)
            otp=random.randint(100000,999999)
            subject="Opt from lnxct"
            message="your forgotepassword otp is "+str(otp)
            send_mail(
                subject,
                message,
                "dummyworkingco@gmail.com", 
                [mail],     
                fail_silently=False,
            )
            if userotp.objects.filter(email=user).exists():
                change=userotp.objects.get(email=user)
                change.otp=otp
                change.save()
            else:
                userotp.objects.create(email=user,otp=otp)
            return Response({'message':'otp has been send your register email address','success':True})
        else:
            return Response({'message':'this email address not register','success':False})

class validateotpforgotepsw(generics.GenericAPIView):
    def post(self,request):
        mail=request.data.get('email')
        otpreq=request.data.get('otp')
        user = CustomUser.objects.get(email=mail)
        change=userotp.objects.filter(email=user,otp=otpreq)
        if change:
            return Response({'message':'otp verify successfully..','success':True})
        else:
            return Response({'message':'Invalid otp','success':False})

class setpassword(generics.GenericAPIView):
    def post(self,request):
        mail=request.data.get('email')
        psw=request.data.get('password')
        change=CustomUser.objects.filter(email=mail)
        if change:
            change=CustomUser.objects.get(email=mail)
            change.password=make_password(psw)
            change.save()
            return Response({'message':'Your password reset successfully..','success':True})
        else:
            return Response({'message':'Password not reset','success':False})
        
class upload_image(generics.CreateAPIView):
    queryset=userimage.objects.all()
    serializer_class=customuserserializer
    def perform_create(self, serializer):
        # Retrieve the email from the request
        mail = self.request.data.get('email')

        # Try to find the user by email
        try:
            user = CustomUser.objects.get(email=mail)
        except CustomUser.DoesNotExist:
            return Response({'message': 'User with this email does not exist', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

        # Add the user to the serializer before saving
        user_image_instance = serializer.save(created_by=user)

        # Now, create the status.json file
        user_uuid = user_image_instance.created_by.id  # The UUID of the user
        tmp_dir = os.path.join(settings.MEDIA_ROOT, 'tmp', str(user_uuid))
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
        return Response({'message': 'User image uploaded successfully', 'success': True}, status=status.HTTP_201_CREATED)
    # def create(self, request, *args, **kwargs):
    #     mail=request.data.get('email')
    #     user = CustomUser.objects.get(email=mail)
    #     img1=request.data.get('img1')
    #     img2=request.data.get('img2')
    #     backgrd=request.data.get('background')
    #     serial=userimgserilizer(data=request.data)
    #     if serial.is_valid():
    #         serial.save()
    #         return Response({'message':'Images is successfully uplodaded','success':True})
    #     return Response({'message':'Images is not uplodaded','success':False})