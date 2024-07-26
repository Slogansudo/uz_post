from models.models import CustomUser
from rest_framework import serializers


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Userlar ro'yhatdan o'tishi uchun mo'ljallangan serializer class
    """
    class Meta:
        model = CustomUser
        fields = ('phone_number', 'first_name', 'last_name', 'password')
