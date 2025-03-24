"""
URL configuration for firstuser project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register',views.register.as_view(),name='register'),
    path('verify',views.verify.as_view(),name='verify'),
    path('login',views.login.as_view(),name='login'),
    path('forgot_password',views.forgotepsw.as_view(),name='forgotepsw'),
    path('validate_otp_forgot_password',views.validateotpforgotepsw.as_view(),name='validateotpforgotepsw'),
    path('set_password',views.setpassword.as_view(),name='setpassword'),
    path('upload_image',views.upload_image.as_view(),name='upload_image'),
    path('get_status_json',views.get_status_json.as_view(),name='get_status_json'),
]
