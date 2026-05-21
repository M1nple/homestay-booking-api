from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser

from users.models import HostRequest
from users.serializers.auth_serializers import HostRequestSerializer


class HostRequestView(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated]

    serializer_class = HostRequestSerializer

    parser_classes = [
        MultiPartParser,
        FormParser
    ]

    def get_queryset(self):

        return HostRequest.objects.filter(
            user=self.request.user
        ).order_by('-created_at')

    def perform_create(self, serializer):

        if HostRequest.objects.filter(
            user=self.request.user,
            status=HostRequest.Status.PENDING
        ).exists():

            raise ValidationError(
                "Bạn đã gửi yêu cầu trở thành host, vui lòng chờ admin phê duyệt."
            )

        if HostRequest.objects.filter(
            user=self.request.user,
            status=HostRequest.Status.APPROVED
        ).exists():

            raise ValidationError(
                "Bạn đã là host, không thể gửi yêu cầu trở thành host nữa."
            )

        serializer.save(
            user=self.request.user
        )