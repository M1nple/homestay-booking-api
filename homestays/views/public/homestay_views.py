from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.viewsets import ReadOnlyModelViewSet
from homestays.models import Homestay
from homestays.serializers.public_serializers import PublicHomestaySerializer

class PublicHomestayViewSet(ReadOnlyModelViewSet): # ReadOnlyModelViewSet Chỉ cho phép xem danh sách và chi tiết homestay, không cho phép tạo, cập nhật hoặc xóa
    queryset = Homestay.objects.filter(deleted_at__isnull=True)
    serializer_class = PublicHomestaySerializer
    # permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        # Lọc homestay theo user hiện tại (host)
        return Homestay.objects.filter(deleted_at__isnull=True)