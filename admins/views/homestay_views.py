from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser

from homestays.models import Homestay

from admins.serializers.homestay_serializers import (
    AdminHomestaySerializer
)


class AdminHomestayListView(ListAPIView):

    queryset = Homestay.objects.all()

    serializer_class = AdminHomestaySerializer

    permission_classes = [IsAdminUser]