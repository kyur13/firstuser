from .models import CustomUser,userimage
from rest_framework.serializers import ModelSerializer

class customuserserializer(ModelSerializer):
    class Meta:
        model=CustomUser
        fields='__all__'

class userimgserilizer(ModelSerializer):
    class Meta:
        model=userimage
        fields='__all__'