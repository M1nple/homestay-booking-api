from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from users.serializer import  HostRequestSerializer
from users.models import User
from rest_framework.parsers import MultiPartParser, FormParser


class HostRequestView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HostRequestSerializer
    queryset = User.objects.all()
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)