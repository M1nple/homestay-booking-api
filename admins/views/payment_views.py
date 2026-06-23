from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.utils import timezone

from bookings.models import Booking

from payments.models import Payment

from admins.serializers.payment_serializers import AdminPaymentSerializer



class AdminPaymentListView(ListAPIView):

    queryset = Payment.objects.all().order_by(
        '-created_at'
    )

    serializer_class = AdminPaymentSerializer

    permission_classes = [IsAdminUser]



class ApproveRefundAPIView(APIView):

    permission_classes = [
        IsAdminUser
    ]

    def patch(
        self,
        request,
        pk
    ):

        try:

            booking = Booking.objects.get(
                pk=pk
            )

        except Booking.DoesNotExist:

            return Response(
                {
                    "detail":
                    "Booking not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if (
            booking.status !=
            Booking.Status.REFUND_PENDING
        ):

            return Response(
                {
                    "detail":
                    "Booking không ở trạng thái chờ hoàn tiền."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        payment = booking.payment

        payment.status = (
            Payment.Status.REFUNDED
        )

        payment.save()

        booking.status = (
            Booking.Status.CANCELLED
        )
        booking.refund_at = timezone.now()

        booking.save()

        return Response(
            {
                "message":
                "Refund approved successfully."
            }
        )