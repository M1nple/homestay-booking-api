# from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from homestays.models import Homestay
from rooms.models import Room
from users.permissions import IsHost


from rooms.serializers.host_serializers import (
    CreateRoomSerializer,
    UpdateRoomSerializer,
    RoomListSerializer,
    RoomDetailSerializer
)


class RoomViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated, IsHost]

    # =========================
    # QUERYSET
    # =========================
    def get_queryset(self):

        return Room.objects.filter(
            homestay_id=self.kwargs['homestay_id'],
            deleted_at__isnull=True,
            homestay__deleted_at__isnull=True,
            homestay__owner=self.request.user
        )

    # =========================
    # SERIALIZER
    # =========================
    def get_serializer_class(self):

        if self.action == 'create':
            return CreateRoomSerializer

        elif self.action in ['update', 'partial_update']:
            return UpdateRoomSerializer

        elif self.action == 'retrieve':
            return RoomDetailSerializer

        return RoomListSerializer

    # =========================
    # CREATE ROOM
    # =========================
    def perform_create(self, serializer):

        homestay = get_object_or_404(
            Homestay, 
            id=self.kwargs['homestay_id'],
            deleted_at__isnull=True
        )

        # optional:
        # check owner permission
        if homestay.owner != self.request.user:
            raise PermissionDenied(
                "Bạn không có quyền thêm phòng"
            )

        serializer.save(homestay=homestay)

    # =========================
    # UPDATE ROOM   
    # =========================
    def perform_update(self, serializer):

        room = self.get_object()

        # optional:
        # check owner permission
        if room.homestay.owner != self.request.user:
            raise PermissionDenied(
                "Bạn không có quyền cập nhật phòng này"
            )
        serializer.save()
    
    # =========================
    # DELETE ROOM   
    # =========================
    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save()