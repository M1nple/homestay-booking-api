from django.db.models import Sum

from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from users.models import User
from homestays.models import Homestay
from rooms.models import Room
from bookings.models import Booking
from payments.models import Payment


class AdminDashboardView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        total_users = User.objects.count()

        total_hosts = User.objects.filter(
            role='HOST'
        ).count()

        total_homestays = Homestay.objects.count()

        total_rooms = Room.objects.count()

        total_bookings = Booking.objects.count()

        total_revenue = (
            Payment.objects.filter(
                status=Payment.Status.SUCCESS
            ).aggregate(
                total=Sum('amount')
            )['total']
            or 0
        )

        return Response({
            'total_users': total_users,
            'total_hosts': total_hosts,
            'total_homestays': total_homestays,
            'total_rooms': total_rooms,
            'total_bookings': total_bookings,
            'total_revenue': total_revenue
        })