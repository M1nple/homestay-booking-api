from rest_framework import serializers
from bookings.models import Booking, BookingRoom


class BookingRoomSerializer(serializers.ModelSerializer):
    room_name = serializers.CharField(
        source='room.name',
        read_only=True
    )

    class Meta:
        model = BookingRoom
        fields = ['room_name']

class BookingSerializer(serializers.ModelSerializer):
    rooms = BookingRoomSerializer(
        many=True,
        read_only=True
    )

    rooms_name = serializers.CharField(
        source='rooms__room__name',
        read_only=True
    )

    homestay_name = serializers.CharField(
        source='homestay.name',
        read_only=True
    )

    user_name = serializers.CharField(
        source='user.username',
        read_only=True
    )
    class Meta:
        model = Booking
        fields = [
            'id',
            'user_name',
            'homestay_name',
            'check_in',
            'check_out',
            'total_guests',
            'total_price',
            'status',
            'rooms',
            'rooms_name'
        ]

class BookingDetailSerializer(serializers.ModelSerializer):
    rooms = BookingRoomSerializer(
        many=True,
        read_only=True
    )

    homestay_name = serializers.CharField(
        source='homestay.name',
        read_only=True
    )

    user_name = serializers.CharField(
        source='user.username',
        read_only=True
    )

    cancelled_by = serializers.CharField(
        source='cancelled_by.username',
        read_only=True
    )

    class Meta:
        model = Booking
        fields = [
            'id',
            'user_name',
            'homestay_name',
            'check_in',
            'check_out',
            'total_guests',
            'total_price',
            'status',
            'rooms',

            'cancelled_at',
            'cancelled_by',
            'cancel_reason',
            'confirm_at'

        ]