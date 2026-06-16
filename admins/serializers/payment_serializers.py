from rest_framework import serializers
from payments.models import Payment


class AdminPaymentSerializer(serializers.ModelSerializer):

    booking_id = serializers.IntegerField(
        source='booking.id',
        read_only=True
    )

    customer = serializers.CharField(
        source='booking.user.full_name',
        read_only=True
    )

    class Meta:
        model = Payment
        fields = [
            'id',
            'booking_id',
            'customer',
            'amount',
            'method',
            'status',
            'created_at'
        ]