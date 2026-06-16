from rest_framework import serializers
from users.models import User

class AdminUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'full_name',
            'email',
            'phone',
            'role',
            'is_verified',
            'is_active',
            'created_at'
        ]