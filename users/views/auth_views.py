from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializer import RegisterSerializer, CustomTokenSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer