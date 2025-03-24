from .models import CustomUser,userimage
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
class customuserserializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields='__all__'

class userimgserilizer(serializers.ModelSerializer):
    class Meta:
        model=userimage
        fields = ['img1', 'img2', 'img3', 'background']