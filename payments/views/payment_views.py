import uuid
import hmac
import hashlib
import urllib.parse

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from bookings.models import Booking, BookingRoom
from payments.models import Payment, PaymentAttempt

from payments.utils import create_vnpay_payment_url


# =====================================================
# CREATE PAYMENT
# =====================================================

class CreateVNPayPaymentView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, booking_id):

        booking = get_object_or_404(
            Booking,
            id=booking_id,
            user=request.user
        )

        # booking phải pending
        if booking.status != Booking.Status.PENDING:

            raise ValidationError(
                'Booking không hợp lệ để thanh toán.'
            )

        # booking hết hạn
        if (
            booking.expired_at
            and
            timezone.now() > booking.expired_at
        ):

            booking.status = Booking.Status.CANCELLED

            booking.cancelled_at = timezone.now()

            booking.cancel_reason = (
                'Quá thời gian thanh toán'
            )

            booking.save()

            return Response({
                'message': 'Booking đã hết hạn thanh toán.'
            }, status=400)

        payment, _ = Payment.objects.get_or_create(

            booking=booking,

            defaults={

                'amount': booking.total_price,

                'method': Payment.Method.VNPAY,

                'status': Payment.Status.PENDING
            }
        )

        # đã thanh toán
        if payment.status == Payment.Status.SUCCESS:

            raise ValidationError(
                'Booking này đã thanh toán.'
            )

        payment_attempt = PaymentAttempt.objects.create(

            payment=payment,

            amount=payment.amount,

            status=Payment.Status.PENDING,

            txn_ref=str(uuid.uuid4()).replace('-', '')[:20]
        )

        payment_url = create_vnpay_payment_url(
            request,
            payment_attempt
        )

        return Response({
            'payment_url': payment_url
        })


# =====================================================
# VNPAY CALLBACK
# =====================================================

class VNPayReturnView(APIView):

    authentication_classes = []
    permission_classes = []

    @transaction.atomic
    def get(self, request):
        input_data = request.GET.dict()
        secure_hash = input_data.pop(
            'vnp_SecureHash',
            None
        )
        if not secure_hash:
            return Response({
                'message': 'Missing secure hash'
            }, status=400)
        input_data.pop(
            'vnp_SecureHashType',
            None
        )
        sorted_data = sorted(
            input_data.items()
        )
        query_string = urllib.parse.urlencode(
            sorted_data
        )
        hash_value = hmac.new(
            settings.VNPAY_HASH_SECRET_KEY.encode(),
            query_string.encode(),
            hashlib.sha512
        ).hexdigest()
        
        # validate checksum
        if hash_value != secure_hash:

            return Response({
                'message': 'Invalid checksum'
            }, status=400)

        txn_ref = input_data.get(
            'vnp_TxnRef'
        )

        response_code = input_data.get(
            'vnp_ResponseCode'
        )

        payment_attempt = (
            PaymentAttempt.objects
            .select_for_update()
            .get(txn_ref=txn_ref)
        )

        payment = payment_attempt.payment

        booking = payment.booking

        # callback duplicate
        if payment.status == Payment.Status.SUCCESS:

            return Response({
                'message': 'Payment already confirmed'
            })

        # validate amount
        amount = int(
            input_data.get(
                'vnp_Amount',
                0
            )
        )

        if amount != int(payment.amount * 100):

            return Response({
                'message': 'Invalid amount'
            }, status=400)

        # booking hết hạn
        if (
            booking.expired_at
            and
            timezone.now() > booking.expired_at
        ):

            booking.status = Booking.Status.CANCELLED

            booking.cancelled_at = timezone.now()

            booking.cancel_reason = (
                'Quá thời gian thanh toán'
            )

            booking.save()

            payment.status = Payment.Status.FAILED

            payment.save()

            payment_attempt.status = Payment.Status.FAILED

            payment_attempt.vnp_response_code = (
                response_code
            )

            payment_attempt.pay_date = timezone.now()

            payment_attempt.save()

            return Response({
                'message': (
                    'Booking đã hết thời gian thanh toán.'
                )
            }, status=400)

        # =================================================
        # PAYMENT SUCCESS
        # =================================================

        if response_code == '00':

            # =============================================
            # CHECK OVERLAP
            # =============================================

            booking_rooms = (
                BookingRoom.objects.filter(
                    booking=booking
                )
            )

            for booking_room in booking_rooms:

                room = booking_room.room

                conflict = (
                    BookingRoom.objects.filter(

                        room=room,

                        booking__status=(
                            Booking.Status.CONFIRMED
                        ),

                        booking__check_in__lt=(
                            booking.check_out
                        ),

                        booking__check_out__gt=(
                            booking.check_in
                        )

                    )
                    .exclude(
                        booking=booking
                    )
                    .exists()
                )

                if conflict:

                    booking.status = (
                        Booking.Status.CANCELLED
                    )

                    booking.cancelled_at = (
                        timezone.now()
                    )

                    booking.cancel_reason = (
                        'Phòng đã được đặt'
                    )

                    booking.save()

                    payment.status = (
                        Payment.Status.FAILED
                    )

                    payment.save()

                    payment_attempt.status = (
                        Payment.Status.FAILED
                    )

                    payment_attempt.vnp_response_code = (
                        response_code
                    )

                    payment_attempt.pay_date = (
                        timezone.now()
                    )

                    payment_attempt.save()

                    return Response({
                        'message': (
                            f'Phòng "{room.name}" '
                            'đã được đặt trước.'
                        )
                    }, status=400)

            # =============================================
            # CONFIRM PAYMENT
            # =============================================

            payment.status = (
                Payment.Status.SUCCESS
            )

            payment.save()

            payment_attempt.status = (
                Payment.Status.SUCCESS
            )

            payment_attempt.vnp_response_code = (
                response_code
            )

            payment_attempt.vnp_transaction_no = (
                input_data.get(
                    'vnp_TransactionNo'
                )
            )

            payment_attempt.bank_code = (
                input_data.get(
                    'vnp_BankCode'
                )
            )

            payment_attempt.pay_date = (
                timezone.now()
            )

            payment_attempt.save()

            booking.status = (
                Booking.Status.CONFIRMED
            )

            booking.confirm_at = (
                timezone.now()
            )

            booking.save()

            # return Response({
            #     'message': 'Payment success'
            # })

            return redirect(
                f"http://127.0.0.1:5500/payment-result.html"
                f"?status=success"
                f"&booking={booking.id}"
            )

        # =================================================
        # PAYMENT FAILED
        # =================================================

        payment.status = (
            Payment.Status.FAILED
        )

        payment.save()

        payment_attempt.status = (
            Payment.Status.FAILED
        )

        payment_attempt.vnp_response_code = (
            response_code
        )

        payment_attempt.pay_date = (
            timezone.now()
        )

        payment_attempt.save()

        return Response({
            'message': 'Payment failed'
        })