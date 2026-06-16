from rest_framework import serializers
from homestays.models import Homestay


class AdminHomestaySerializer(serializers.ModelSerializer):

    owner_name = serializers.CharField(
        source='owner.full_name',
        read_only=True
    )

    class Meta:
        model = Homestay
        fields = [
            'id',
            'name',
            'owner_name',
            'address',
            'province',
            'district',
            'ward',
            'created_at',
            'updated_at',
            'deleted_at',
        ]