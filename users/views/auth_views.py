from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializer import RegisterSerializer, CustomTokenSerializer, UpdateUserSerializer, UserSerializer, LogoutSerializer, HostRequestSerializer
from rest_framework.views import APIView 
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User

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
    


