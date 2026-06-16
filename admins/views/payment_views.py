from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser

from payments.models import Payment

from admins.serializers.payment_serializers import (
    AdminPaymentSerializer
)


class AdminPaymentListView(ListAPIView):

    queryset = Payment.objects.all().order_by(
        '-created_at'
    )

    serializer_class = AdminPaymentSerializer

    permission_classes = [IsAdminUser]