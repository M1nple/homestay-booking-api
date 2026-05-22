from django.utils import timezone

from django.db import transaction

from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from users.permissions import IsHost

from bookings.models import Booking

from bookings.serializers.host_serializers import BookingSerializer, BookingDetailSerializer

class HostBookingViewSet(    
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,

    GenericViewSet
    ):

    permission_classes = [IsAuthenticated, IsHost]

    def get_queryset(self):

        queryset = Booking.objects.filter(
            homestay__owner=self.request.user,
        )

        status = self.request.query_params.get('status')

        if status:
            queryset = queryset.filter(
                status=status
            )

        return queryset.order_by('-created_at')

    def get_serializer_class(self):
        if self.action in ['list']:
            return BookingSerializer
        elif self.action in ['retrieve']:
            return BookingDetailSerializer
        return BookingSerializer

    @action(detail=True, methods=['patch'])
    def confirm(self, request, pk=None):

        booking = self.get_object()

        # chỉ cho phép xác nhận booking đang chờ xử lý
        if booking.status != Booking.Status.PENDING:

            return Response(
                {
                    'detail': 'Booking này không thể xác nhận.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():

            booking.status = Booking.Status.CONFIRMED
            booking.confirm_at = timezone.now()
            booking.save()

        return Response(
            {
                'detail': 'Booking đã được xác nhận.'
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['patch'])
    def reject(self, request, pk=None):
        booking = self.get_object()

        # chỉ cho phép từ chối booking đang chờ xử lý
        if booking.status != Booking.Status.PENDING:

            return Response(
                {
                    'detail': 'Booking này không thể từ chối.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():

            booking.status = Booking.Status.CANCELLED
            booking.cancelled_at = timezone.now()
            booking.cancelled_by = request.user
            booking.cancel_reason = 'Bị từ chối bởi chủ nhà.'
            booking.save()

        return Response(
            {
                'detail': 'Booking đã bị từ chối.'
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['patch'])
    def complete(self, request, pk=None):

        booking = self.get_object()

        if booking.check_out > timezone.now().date():

            return Response(
                {
                    'detail': 'Chưa đến ngày checkout.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # chỉ booking CONFIRMED mới được complete
        if booking.status != Booking.Status.CONFIRMED:

            return Response(
                {
                    'detail': 'Chỉ booking CONFIRMED mới có thể hoàn thành.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = Booking.Status.COMPLETED

        booking.save()

        return Response(
            {
                'message': 'Booking đã hoàn thành.'
            },
            status=status.HTTP_200_OK
        )