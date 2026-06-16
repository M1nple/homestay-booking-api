from rest_framework import serializers
from payments.models import Payment


class HostPaymentSerializer(serializers.ModelSerializer):

    booking_id = serializers.IntegerField(
        source='booking.id',
        read_only=True
    )

    class Meta:
        model = Payment
        fields = [
            'id',
            'booking_id',
            'amount',
            'status',
            'created_at'
        ]