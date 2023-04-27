# ftchat/serializers.py

from rest_framework import serializers
from .models import Message, User


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id', 'username', 'password', 'email', 'phone_number', 'avatar', 'bio',
            'created_at', 'last_login_at', 'sentiment_analysis_enabled'
        ]
