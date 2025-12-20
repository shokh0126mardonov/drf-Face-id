from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Student,Rules

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['groups', 'user_permissions', 'is_staff', 'is_superuser', 'last_login','password','role','date_joined','is_active']


class RegisterSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128)

class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        exclude = ['password', 'role', 'groups', 'user_permissions', 'is_staff', 'is_superuser']
        extra_kwargs = {
            'username': {
                'required': False
            }
        }

class PasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128)
    confirm = serializers.CharField(max_length=128)

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm']:
            raise serializers.ValidationError('Password va confirm teng emas!')
        return super().validate(attrs)
    
class StudentSerializers(serializers.ModelSerializer):

    class Meta:
        model = Student
        exclude = ['created_at','updated_at']
        
    admin = UserSerializer(read_only=True)

class RulesSerializers(serializers.ModelSerializer):
    admin = UserSerializer(read_only=True)
    
    class Meta:
        model = Rules
        fields = ['id','gender','time','exit_time','admin']