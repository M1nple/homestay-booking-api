from models import Homestay
from users.permissions import IsHost
from homestays.serializer import HomestaySerializer
from rest_framework import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

class HomestayViewSet(ModelViewSet):
    queryset = Homestay.objects.all()
    serializer_class = HomestaySerializer
    permission_classes = [IsAuthenticated, IsHost]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        # Lọc homestay theo user hiện tại (host)
        user = self.request.user
        return Homestay.objects.filter(host=user)
    
    def perform_create(self, serializer):
        # Gán host là user hiện tại khi tạo homestay mới
        serializer.save(host=self.request.user)
        
    