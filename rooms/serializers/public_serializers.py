from rest_framework import serializers
from rest_framework.generics import ListAPIView

from bookings.models import Booking, BookingRoom
from ..models import Room, RoomImage
from django.db.models import Avg
from reviews.serializers.review_serializers import ReviewSerializer

class RoomImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomImage
        fields = ['id', 'image_url']

class PublicRoomSerializer(serializers.ModelSerializer):
    images = RoomImageSerializer(many=True, read_only=True)
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = [
            'id',
            'name',
            'price',
            'capacity',
            # 'description',
            'images',
            # 'homestay',
            'avg_rating',
        ]
    def get_avg_rating(self, obj):

        return obj.reviews.aggregate(
            avg=Avg('rating')
        )['avg']
    
class PublicRoomDetailSerializer(serializers.ModelSerializer):
    images = RoomImageSerializer(many=True, read_only=True)

    reviews = ReviewSerializer(
        many=True,
        read_only=True
    )

    amenities_names = serializers.StringRelatedField(
        source='amenities',
        many=True,
        read_only=True)
    

    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = [
            'id',
            'name',
            'price',
            'capacity',
            'description',
            'images',
            'homestay',
            'amenities',
            'amenities_names',
            'avg_rating',
            'reviews'
        ]
    def get_avg_rating(self, obj):

        return obj.reviews.aggregate(
            avg=Avg('rating')
        )['avg']
    

    class AvailableRoomView(ListAPIView):

        serializer_class = PublicRoomSerializer

        def get_queryset(self):

            homestay_id = self.request.query_params.get(
                'homestay_id'
            )

            check_in = self.request.query_params.get(
                'check_in'
            )

            check_out = self.request.query_params.get(
                'check_out'
            )

            queryset = Room.objects.filter(
                homestay_id=homestay_id,
                deleted_at__isnull=True,
                status=Room.Status.AVAILABLE
            )

            booked_rooms = BookingRoom.objects.filter(
                booking__status__in=[
                    Booking.Status.PENDING,
                    Booking.Status.CONFIRMED
                ],
                booking__check_in__lt=check_out,
                booking__check_out__gt=check_in
            ).values_list(
                'room_id',
                flat=True
            )

            return queryset.exclude(
                id__in=booked_rooms
            )