from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from users.permissions import IsAdmin
from users.serializers.admin_serializers import HostRequestserializer, RejectHostRequestSerializer

from ..models import HostRequest, HostProfile

class HostRequestViewSet(mixins.ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser, IsAdmin]
    serializer_class = HostRequestserializer

    def get_queryset(self):
        queryset = HostRequest.objects.all()
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(
                status=status
            )
        return queryset.order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return HostRequestserializer
        return super().get_serializer_class()
    
# Admin có thể phê duyệt hoặc từ chối yêu cầu trở thành host của user
    @action(detail=True, methods=['post'], url_path='approve')
    @transaction.atomic
    def approve(self, request, pk=None):
        host_request = self.get_object()
        host_request = get_object_or_404(HostRequest, pk = pk, status = 'PENDING')

    # Tạo host profile
        HostProfile.objects.get_or_create( # get_or_create kiểm tra nếu đã tồn tại host profile cho user này chưa, nếu chưa thì tạo mới, nếu đã tồn tại thì trả về host profile đó
            user = host_request.user,
            status = HostProfile.Status.ACTIVE,
            approved_at = timezone.now(),
            approved_by = request.user,
            defaults = {
                'business_name': host_request.business_name,
                'description': host_request.description,
                'avatar_url': host_request.identity_image.url if host_request.identity_image else None,
                'identity_number': host_request.identity_number,
                'identity_image': host_request.identity_image.url if host_request.identity_image else None,
            }

        )
    # Cập nhật trạng thái của host request
        host_request.status = HostRequest.Status.APPROVED
        host_request.reviewed_by = request.user
        host_request.reviewed_at = timezone.now()
        host_request.save()

    # câp nhật role của user thành host
        user = host_request.user
        user.role = 'HOST'
        user.save(update_fields=['role'])
        return Response({'message': 'Yêu cầu trở thành host đã được phê duyệt.'}, status=status.HTTP_200_OK)
    
    
    def get_serializer_class(self):
        if self.action == 'reject':
            return RejectHostRequestSerializer
        return HostRequestserializer
    @action(
        detail=True,
        methods=['post'],
        url_path='reject'
    )
    @transaction.atomic
    def reject(self, request, pk=None):
        host_request = self.get_object()
        serializer = self.get_serializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True) 
        host_request.status = HostRequest.Status.REJECTED
        host_request.rejection_reason = serializer.validated_data[
            'rejection_reason'
        ]

        host_request.reviewed_by = request.user
        host_request.reviewed_at = timezone.now()
        host_request.save()
        return Response({
            'message': 'Yêu cầu trở thành host đã bị từ chối.'
        })