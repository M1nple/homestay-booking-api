from django.db.models import Min
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny 
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.viewsets import ReadOnlyModelViewSet
from rooms.models import Room
from rooms.serializers.public_serializers import PublicRoomSerializer

class PublicRoomViewSet(ReadOnlyModelViewSet): # ReadOnlyModelViewSet Chỉ cho phép xem danh sách và chi tiết phòng, không cho phép tạo, cập nhật hoặc xóa
    queryset = Room.objects.filter(deleted_at__isnull=True)
    serializer_class = PublicRoomSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    search_fields = ["homestay__name", "province__name", "district__name", "ward__name"] 

    filterset_fields = ['capacity', 'homestay']

    ordering_fields = ["price"]

    ordering = ["price"]

    def get_queryset(self):
        # Lọc phòng theo user hiện tại (host)
        queryset = Room.objects.filter(deleted_at__isnull=True).annotate(
            min_price=Min('price')  # Lọc phòng có giá thấp nhất lớn hơn hoặc bằng giá tối thiểu
        )
            # Lọc phòng theo khoảng giá thấp nhất
        min_price = self.request.query_params.get('min_price')
        if min_price:
            return self.queryset.filter(price__gte=min_price) # Lọc phòng có giá thấp nhất lớn hơn hoặc bằng giá tối thiểu

            # Lọc phòng theo khoảng giá cao nhất
        max_price = self.request.query_params.get('max_price')
        if max_price:
            return self.queryset.filter(price__lte=max_price) # Lọc phòng có giá thấp nhất nhỏ hơn hoặc bằng giá tối đa

        return queryset.distinct() # distinct loại bỏ dữ liệu trùng lặp Tránh trùng lặp phòng khi có nhiều phòng cùng giá thấp nhất trong một homestay