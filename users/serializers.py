from typing import Any, Dict
from rest_framework import serializers
from django.core.mail import send_mail
from .models import UserModel
from conf.settings import EMAIL_HOST
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password
class UserRegisterSreializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = UserModel
        fields = ['email', 'username', 'last_name', 'first_name', 'password', 'confirm_password']
        
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError('Password does not match')
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        
        user = super(UserRegisterSreializer, self).create(validated_data)
        code = user.create_verify_code()
        
        send_mail(
            from_email=EMAIL_HOST,
            recipient_list=[user.email],
            subject="Activation code",
            message=f"Your activation code is {code}"
        )
        print(code)
        user.set_password(validated_data['password'])
        user.save()
        return user 
    
class LoginSerializer(TokenObtainPairSerializer):
    password = serializers.CharField(max_length=128, required=True, write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        
        user = UserModel.objects.filter(username=username).first()

        if user is None:
            raise serializers.ValidationError({
                "success": False,
                "message": "Foydalanuvchi topilmadi"
            })

        auth_user = authenticate(username=user.username, password=password)
    
        if not auth_user:
            raise serializers.ValidationError({
                "success": False,
                "message": "Noto'g'ri parol",
            })

        refresh = RefreshToken.for_user(auth_user)

        return {
            'success': True,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }
    
class UpdateUserSerializer(serializers.Serializer):
    
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    
    def validate(self, email):
        
        if not email.get('email').endswith('@gmail.com'):
            raise serializers.ValidationError('Email must be gmail.com')
        
        return email
    
    def validate_username(self, username):
        
        if len(username) < 4 or len(username) > 55:
            raise serializers.ValidationError('Username must be between 4 and 55 characters')
        
        if username.isdigit():
            raise serializers.ValidationError('Username must be string')
        
        return username
    
    
    
    def update(self, instance, validated_data):
        
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        
        instance.save()
        return instance
            