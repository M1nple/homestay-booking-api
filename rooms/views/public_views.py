from django.db.models import Min

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from rooms.models import Room
from bookings.models import Booking, BookingRoom

from rooms.serializers.public_serializers import (
    PublicRoomSerializer,
    PublicRoomDetailSerializer
)


class PublicRoomViewSet(ReadOnlyModelViewSet):
    queryset = Room.objects.filter(
        deleted_at__isnull=True
    )
    permission_classes = [AllowAny]
    parser_classes = [
        MultiPartParser,
        FormParser
    ]
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]
    search_fields = [
        'name',
        'homestay__name',
    ]
    filterset_fields = [
        'capacity',
        'homestay',
    ]
    ordering_fields = [
        'price'
    ]
    ordering = [
        'price'
    ]
    def get_queryset(self):
        queryset = Room.objects.filter(
            deleted_at__isnull=True
        ).annotate(
            min_price=Min('price')
        )
        min_price = self.request.query_params.get(
            'min_price'
        )
        max_price = self.request.query_params.get(
            'max_price'
        )
        if min_price:
            queryset = queryset.filter(
                price__gte=min_price
            )
        if max_price:
            queryset = queryset.filter(
                price__lte=max_price
            )
        return queryset.distinct()
    def get_serializer_class(self):
        if self.action == 'list':
            return PublicRoomSerializer
        if self.action == 'retrieve':
            return PublicRoomDetailSerializer
        return PublicRoomSerializer
    
    @action(
        detail=False,
        methods=['get'],
        url_path='available'
    )

    def available(self, request):
        homestay_id = request.query_params.get(
            'homestay_id'
        )
        check_in = request.query_params.get(
            'check_in'
        )
        check_out = request.query_params.get(
            'check_out'
        )
        if not homestay_id:
            raise ValidationError(
                {
                    'homestay_id':
                    'homestay_id là bắt buộc.'
                }
            )
        if not check_in:
            raise ValidationError(
                {
                    'check_in':
                    'check_in là bắt buộc.'
                }
            )
        if not check_out:
            raise ValidationError(
                {
                    'check_out':
                    'check_out là bắt buộc.'
                }
            )
        rooms = Room.objects.filter(
            homestay_id=homestay_id,
            deleted_at__isnull=True,
            status=Room.Status.AVAILABLE
        )
        booked_room_ids = (
            BookingRoom.objects.filter(
                booking__status__in=[
                    Booking.Status.PENDING,
                    Booking.Status.CONFIRMED
                ],
                booking__check_in__lt=check_out,
                booking__check_out__gt=check_in
            )
            .values_list(
                'room_id',
                flat=True
            )
        )
        available_rooms = rooms.exclude(
            id__in=booked_room_ids
        )
        serializer = PublicRoomSerializer(
            available_rooms,
            many=True
        )
        return Response(serializer.data)