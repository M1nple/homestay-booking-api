from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser

from users.models import User

from admins.serializers.user_serializers import (
    AdminUserSerializer
)


class AdminUserListView(ListAPIView):

    queryset = User.objects.all()

    serializer_class = AdminUserSerializer

    permission_classes = [IsAdminUser]