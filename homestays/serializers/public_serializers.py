from rest_framework import serializers
from ..models import Homestay, HomestayImage

class HomestayImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = HomestayImage
        fields = ['id', 'image_url']

class PublicHomestaySerializer(serializers.ModelSerializer):

    # custom serializer field để hiển thị tên tỉnh thành, quận huyện, xã phường thay vì chỉ hiển thị ID
    province_name = serializers.CharField(
        source='province.name',
        read_only=True
    )
    district_name = serializers.CharField(
        source='district.name',
        read_only=True
    )
    ward_name = serializers.CharField(
        source='ward.name',
        read_only=True
    )

    images = HomestayImageSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Homestay
        fields = [
                'id',
                'name', 
                'address', 
                'description', 
                'province_name', 
                'district_name',
                'ward_name',
                'images'
                ]