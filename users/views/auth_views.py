from rest_framework import generics, status
from rest_framework.response import Response 
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView 
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers.auth_serializers import RegisterSerializer, CustomTokenSerializer, UpdateUserSerializer, UserSerializer, LogoutSerializer, HostRequestSerializer
from users.serializers.auth_serializers import VerifyEmailSerializer
from users.models import User
from users.models import User,EmailOTP
from users.serializers.auth_serializers import ResendOTPSerializer
from users.utils import generate_and_send_otp
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings






class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]  # Cho phép mọi người có thể đăng ký

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer
    permission_classes = [AllowAny]  # Cho phép mọi người có thể đăng nhập
    
class MeView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user
    
class UpdateUserView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateUserSerializer  
    queryset = User.objects.all()
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user  # Trả về người dùng hiện tại để cập nhật thông tin
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = serializer.validated_data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response({"error": "Invalid token"}, status=400)

        return Response({"message": "Logout successful"}, status=200)
    
class VerifyEmailView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        serializer = (
            VerifyEmailSerializer(
                data=request.data
            )
        )
        serializer.is_valid(
            raise_exception=True
        )
        email = serializer.validated_data[
            'email'
        ]
        otp = serializer.validated_data[
            'otp'
        ]
        user = User.objects.get(
            email=email
        )
        otp_obj = EmailOTP.objects.filter(

            user=user,

            otp_code=otp,

            is_used=False
        ).order_by('-created_at').first()
        if not otp_obj:
            raise ValidationError(
                'OTP không hợp lệ.'
            )
        if timezone.now() > otp_obj.expired_at:
            raise ValidationError(
                'OTP đã hết hạn.'
            )
        user.is_verified = True
        user.save()
        otp_obj.is_used = True
        otp_obj.save()

        send_mail(
            subject='Email Verified',
            message=(
                'Tài khoản của bạn đã được '
                'xác thực thành công.'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        return Response({
            'message': (
                'Xác thực email thành công.'
            )
        })

class ResendOTPView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        serializer = ResendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.filter(email=email).first()

        if not user:
            raise ValidationError(
                'Email không tồn tại.'
            )
        if user.is_verified:

            raise ValidationError(
                'Email đã xác thực.'
            )
        generate_and_send_otp(user)
        return Response({
            'message': 'OTP mới đã được gửi.'
        })