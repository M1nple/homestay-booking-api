from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from rooms.models import Amenity
from rooms.serializers.amenity_serializers import AmenitySerializer


class AmenityViewSet(ModelViewSet):
    queryset = Amenity.objects.all().order_by("id")
    serializer_class = AmenitySerializer
    permission_classes = [IsAuthenticated]