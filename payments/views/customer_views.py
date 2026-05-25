from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from payments.models import Payment

from payments.serializers.customer_serializers import (
    PaymentSerializer,
    PaymentDetailSerializer
)


class CustomerPaymentViewSet(
    ReadOnlyModelViewSet
):

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        queryset = Payment.objects.filter(
            booking__user=self.request.user
        ).select_related(
            'booking',
            'booking__homestay'
        ).prefetch_related(
            'attempts'
        ).order_by('-created_at')

        status = self.request.query_params.get(
            'status'
        )

        if status:

            queryset = queryset.filter(
                status=status
            )

        return queryset

    def get_serializer_class(self):

        if self.action == 'retrieve':

            return PaymentDetailSerializer

        return PaymentSerializer