from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from payments.models import Payment
from payments.serializers.host_serializers import HostPaymentSerializer

from users.permissions import IsHost


class HostPaymentView(APIView):

    permission_classes = [IsAuthenticated, IsHost]


    def get(self, request):

        payments = (
            Payment.objects
            .filter(
                status=Payment.Status.SUCCESS,
                booking__homestay__owner=request.user
            )

            .distinct()
            .order_by('-created_at')
        )
        print(request.user)

        total_revenue = (
            payments.aggregate(
                total=Sum('amount')
            )['total']
            or 0
        )

        serializer = HostPaymentSerializer(
            payments,
            many=True
        )

        return Response({
            'total_revenue': total_revenue,
            'total_transactions': payments.count(),
            'payments': serializer.data
        })