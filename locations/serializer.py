from rest_framework import serializers
from .models import Province, District, Ward

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'code', 'name']

class DistrictSerializer(serializers.ModelSerializer):
    # province = ProvinceSerializer(read_only=True)

    class Meta:
        model = District
        fields = ['id', 'code', 'name', 'province']


class WardSerializer(serializers.ModelSerializer):
    # district = DistrictSerializer(read_only=True)

    class Meta:
        model = Ward
        fields = ['id', 'code', 'name', 'district']