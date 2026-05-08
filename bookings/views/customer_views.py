from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from django.db import transaction
from bookings.models import Booking
from bookings.serializers.customer_serializers import CreateBookingSerializer, BookingDetailSerializer

# class BookingViewSet(ModelViewSet):
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Booking.objects.filter(user=self.request.user)
    
#     def get_serializer_class(self):
#         if self.action == 'create':
#             return CreateBookingSerializer


class BookingViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Booking.objects.filter(
            user=self.request.user
        )

    def get_serializer_class(self):

        if self.action == 'create':
            return CreateBookingSerializer

        return BookingDetailSerializer