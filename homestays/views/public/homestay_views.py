from django.db.models import Min
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.viewsets import ReadOnlyModelViewSet

from homestays.models import Homestay
from homestays.serializers.public_serializers import PublicHomestaySerializer

class PublicHomestayViewSet(ReadOnlyModelViewSet): # ReadOnlyModelViewSet Chỉ cho phép xem danh sách và chi tiết homestay, không cho phép tạo, cập nhật hoặc xóa
    queryset = Homestay.objects.filter(deleted_at__isnull=True)
    serializer_class = PublicHomestaySerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]  # Cho phép tất cả người dùng truy cập
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    search_fields = ['name', 'address', 'province__name', 'district__name', 'ward__name']

    filterset_fields = ['province_id', 'district_id', 'ward_id']

    ordering_fields = ['created_at']

    ordering = ['-created_at']  # Sắp xếp theo ngày tạo mới nhất

    def get_queryset(self):
        # Lọc homestay theo user hiện tại (host)
        # return Homestay.objects.filter(deleted_at__isnull=True)
        queryset = Homestay.objects.filter(
            deleted_at__isnull=True
            ).annotate( 
                min_price=Min('rooms__price')
            )
        
        # Lọc homestay theo số lượng khách yêu cầu
        guests = self.request.query_params.get('guests')
        if guests:
            queryset = queryset.filter( rooms__capacity__gte=guests ) # Lọc homestay có phòng đủ sức chứa lon hon | bang cho số lượng khách yêu cầu

        # Lọc homestay theo khoảng giá thấp nhất
        min_price = self.request.query_params.get('min_price')
        if min_price:
            queryset = queryset.filter( min_price__gte=min_price ) # Lọc homestay có giá thấp nhất lớn hơn hoặc bằng giá tối thiểu

        # Lọc homestay theo khoảng giá cao nhất
        max_price = self.request.query_params.get('max_price')
        if max_price:
            queryset = queryset.filter( min_price__lte=max_price ) # Lọc homestay có giá thấp nhất nhỏ hơn hoặc bằng giá tối đa
        
        return queryset.distinct()