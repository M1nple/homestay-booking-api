from rest_framework import serializers
from ..models import HostRequest

class HostRequestserializer(serializers.ModelSerializer):
    class Meta:
        model = HostRequest
        fields = "__all__"


class RejectHostRequestSerializer(serializers.Serializer):

    rejection_reason = serializers.CharField()