from django.shortcuts import render
from .models import CustomUser,userotp
from .serializer import customuserserializer
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status 
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
import random
class register(APIView):
    def post(self,request):
        mail=request.data.get('email')
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
        if userotp.objects.filter(email=mail).exists():
            change=userotp.objects.get(email=mail)
            change.otp=otp
            change.save()
        else:
            userotp.objects.create(email=mail,otp=otp)
        serial=customuserserializer(data=request.data)
        if serial.is_valid():
            password = serial.validated_data.get('password')
            serial.validated_data['password']=make_password(password)
            serial.validated_data['username']=mail.split('@')[0]
            serial.validated_data['is_active']=False
            serial.save()
            return Response({'message':'user register successfully..','success':True})
        return Response({'message':'user not register','success':False})

class verify(APIView):
    def post(self,request):
        mail=request.data.get('email')
        otpreq=request.data.get('otp')
        change=userotp.objects.filter(email=mail,otp=otpreq)
        if change:
            change=CustomUser.objects.get(email=mail)
            change.is_active=True
            return Response({'message':'user verify successfully..','success':True})
        else:
            return Response({'message':'Invalid otp','success':False})

class login(APIView):
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
    
class forgotepsw(APIView):
    def post(self,request):
        mail=request.data.get('email')
        if CustomUser.objects.filter(email=mail).exists():
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
            if userotp.objects.filter(email=mail).exists():
                change=userotp.objects.get(email=mail)
                change.otp=otp
                change.save()
            else:
                userotp.objects.create(email=mail,otp=otp)
            return Response({'message':'otp has been send your register email address','success':True})
        else:
            return Response({'message':'this email address not register','success':False})

class validateotpforgotepsw(APIView):
    def post(self,request):
        mail=request.data.get('email')
        otpreq=request.data.get('otp')
        change=userotp.objects.filter(email=mail,otp=otpreq)
        if change:
            return Response({'message':'otp verify successfully..','success':True})
        else:
            return Response({'message':'Invalid otp','success':False})

class setpassword(APIView):
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