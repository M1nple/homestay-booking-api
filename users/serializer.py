from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User, HostRequest, HostProfile

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'full_name', 'phone', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # hash password
        user.save()
        return user

# Custom Token Serializer để sử dụng email thay vì username
class CustomTokenSerializer(TokenObtainPairSerializer):
    username_field = 'email'


class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'phone', 'avatar_url', 'role']

    def get_avatar_url(self, obj):
        if obj.avatar_url:
            return obj.avatar_url.url
        return None
    

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'phone', 'avatar_url']
    

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class HostRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostRequest
        fields = ['business_name', 'description', 'identity_number', 'identity_image', 'reason']