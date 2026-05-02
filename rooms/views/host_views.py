from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from homestays.models import Homestay
from rooms.models import Room

from rooms.serializer import (
    CreateRoomSerializer,
    UpdateRoomSerializer,
    RoomListSerializer,
    RoomDetailSerializer
)


class RoomViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated]

    # =========================
    # QUERYSET
    # =========================
    def get_queryset(self):

        return Room.objects.filter(
            homestay_id=self.kwargs['homestay_id'],
            deleted_at__isnull=True
        )

    # =========================
    # SERIALIZER
    # =========================
    def get_serializer_class(self):

        if self.action == 'create':
            return CreateRoomSerializer

        # elif self.action in ['update', 'partial_update']:
        #     return UpdateRoomSerializer

        # elif self.action == 'retrieve':
        #     return RoomDetailSerializer

        # return RoomListSerializer

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