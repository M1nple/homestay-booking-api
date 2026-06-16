from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser

from bookings.models import Booking

from admins.serializers.booking_serializers import (
    AdminBookingSerializer
)


class AdminBookingListView(ListAPIView):

    queryset = Booking.objects.all().order_by(
        '-created_at'
    )

    serializer_class = AdminBookingSerializer

    permission_classes = [IsAdminUser]