from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from ..models import User, HostRequest, HostProfile
from users.utils import generate_and_send_otp

# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         model = User
#         fields = ['email', 'full_name', 'phone', 'password']

#     def create(self, validated_data):
#         password = validated_data.pop('password')
#         user = User(**validated_data)
#         user.set_password(password)  # hash password
#         user.save()
#         is_verified=False
#         generate_and_send_otp(user)
#         return user

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'full_name',
            'email',
            'password',
            'phone',
        ]
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }
    def validate_email(self, value):
        email = value.lower()
        verified_user = User.objects.filter(
            email=email,
            is_verified=True
        ).exists()
        if verified_user:
            raise serializers.ValidationError(
                'Email đã tồn tại.'
            )
        return email
    def create(self, validated_data):
        email = validated_data['email']
        existing_user = User.objects.filter(
            email=email
        ).first()
        # email đã tồn tại nhưng chưa verify
        if existing_user:
            # update thông tin mới nếu muốn
            existing_user.email = validated_data.get(
                'email',
                existing_user.email
            )
            existing_user.phone_number = validated_data.get(
                'phone_number',
                existing_user.phone_number
            )
            password = validated_data.get(
                'password'
            )
            if password:

                existing_user.set_password(
                    password
                )
            existing_user.save()

            generate_and_send_otp(
                existing_user
            )
            return existing_user

        # tạo user mới
        password = validated_data.pop(
            'password'
        )

        user = User.objects.create_user(

            password=password,

            is_verified=False,

            **validated_data
        )

        generate_and_send_otp(user)

        return user

# Custom Token Serializer để sử dụng email thay vì username
class CustomTokenSerializer(TokenObtainPairSerializer):
    username_field = 'email'
    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_verified:
            raise serializers.ValidationError(
                'Email chưa xác thực.'
            )
        return data

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

        def validate(self, data):

            user = self.context['request'].user

            if HostRequest.objects.filter(
                user=user,
                status=HostRequest.Status.PENDING
            ).exists():

                raise serializers.ValidationError(
                    "Bạn đã gửi yêu cầu trước đó."
                )

            if HostRequest.objects.filter(
                user=user,
                status=HostRequest.Status.APPROVED
            ).exists():

                raise serializers.ValidationError(
                    "Bạn đã là host."
                )

            return data
        
class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()