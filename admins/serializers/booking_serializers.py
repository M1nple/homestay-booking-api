from rest_framework import serializers
from bookings.models import Booking


class AdminBookingSerializer(serializers.ModelSerializer):

    user_name = serializers.CharField(
        source='user.full_name',
        read_only=True
    )

    homestay_name = serializers.CharField(
        source='homestay.name',
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
            'created_at',
            'confirm_at',
            'created_at',
            'expired_at',

        ]