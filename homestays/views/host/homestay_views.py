from django.utils import timezone
from users.permissions import IsHost
from homestays.models import Homestay
from homestays.serializer import HomestaySerializer, HomestayDetailSerializer,MyHomestaySerializer, UpdateHomestaySerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

class HomestayViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsHost]
    queryset = Homestay.objects.all()
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        # Lọc homestay theo user hiện tại (host)
        user = self.request.user
        return Homestay.objects.filter(owner=user, deleted_at__isnull=True)
        
    
    def get_serializer_class(self):

        if self.action == 'create':
            return HomestaySerializer

        elif self.action in ['update', 'partial_update']:
            return UpdateHomestaySerializer

        elif self.action == 'retrieve':
            return HomestayDetailSerializer

        return MyHomestaySerializer

    def perform_create(self, serializer):
        # Gán owner là user hiện tại khi tạo homestay mới
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        homestay = self.get_object()
        if homestay.owner != self.request.user:
            raise PermissionDenied("Bạn không có quyền sửa homestay này")

        serializer.save()

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save()