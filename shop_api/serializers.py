from rest_framework import serializers
from .models import shop
from core.models import CustomUser

class Shop_Serializer(serializers.ModelSerializer):

    class Meta:

        model = shop
        fields = '__all__' 

    
class User_Serializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:

        model = CustomUser
        fields = (
            'username',
            'email',
            'phone_no',
            'password'
           
        ) 



