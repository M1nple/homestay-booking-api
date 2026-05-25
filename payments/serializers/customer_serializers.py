from rest_framework import serializers

from payments.models import Payment, PaymentAttempt


class PaymentSerializer(serializers.ModelSerializer):

    booking_id = serializers.IntegerField(
        source='booking.id',
        read_only=True
    )

    homestay_name = serializers.CharField(
        source='booking.homestay.name',
        read_only=True
    )

    class Meta:

        model = Payment

        fields = [
            'id',
            'booking_id',
            'homestay_name',
            'amount',
            'method',
            'status',
            'created_at'
        ]




class PaymentAttemptSerializer(serializers.ModelSerializer):

    class Meta:

        model = PaymentAttempt

        fields = [
            'txn_ref',
            'vnp_transaction_no',
            'vnp_response_code',
            'bank_code',
            'pay_date',
            'status',
            'created_at'
        ]


class PaymentDetailSerializer(serializers.ModelSerializer):

    attempts = PaymentAttemptSerializer(
        many=True,
        read_only=True
    )

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
            'method',
            'status',
            'created_at',
            'attempts'
        ]