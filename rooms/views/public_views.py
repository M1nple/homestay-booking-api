from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.viewsets import ReadOnlyModelViewSet
from rooms.models import Room
from rooms.serializers.public_serializers import PublicRoomSerializer

class PublicRoomViewSet(ReadOnlyModelViewSet): # ReadOnlyModelViewSet Chỉ cho phép xem danh sách và chi tiết phòng, không cho phép tạo, cập nhật hoặc xóa
    queryset = Room.objects.filter(deleted_at__isnull=True)
    serializer_class = PublicRoomSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        # Lọc phòng theo user hiện tại (host)
        return Room.objects.filter(deleted_at__isnull=True)

