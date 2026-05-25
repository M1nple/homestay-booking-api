from django.utils import timezone

from django.db import transaction

from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from bookings.models import Booking

from bookings.serializers.customer_serializers import CreateBookingSerializer, BookingSerializer, BookingDetailSerializer



class CustomerBookingViewSet(    
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,

    GenericViewSet
    ):

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        queryset = Booking.objects.filter(
            user=self.request.user
        ).order_by('-created_at')

        status = self.request.query_params.get('status')

        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def get_serializer_class(self):
        if self.action == 'create':

            return CreateBookingSerializer

        elif self.action in ['retrieve']:

            return BookingDetailSerializer

        return BookingSerializer


    @action(detail=True, methods=['patch'])
    def cancel(self, request, pk=None):

        booking = self.get_object()

        # chỉ cho phép hủy booking chưa hoàn thành
        if booking.status not in [
            Booking.Status.PENDING,
            Booking.Status.CONFIRMED
        ]:

            return Response(
                {
                    'detail': 'Booking này không thể hủy.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # cập nhật trạng thái
        booking.status = Booking.Status.CANCELLED

        booking.cancelled_at = timezone.now()

        booking.cancelled_by = request.user

        booking.save()

        return Response(
            {
                'message': 'Hủy booking thành công.'
            },
            status=status.HTTP_200_OK
        )

