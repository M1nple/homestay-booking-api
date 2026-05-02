from rest_framework import serializers
from .models import Homestay, HomestayImage

class HomestaySerializer(serializers.ModelSerializer):

    # custom serializer field vì model không có trường images, 
    # nên phải tạo thủ công để lấy dữ liệu ảnh từ model HomestayImage thông qua related_name 'images'
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
        )
    
    class Meta:
        model = Homestay
        fields = [
                'name', 
                'address', 
                'description', 
                'province', 
                'district',
                'ward',
                'images'
                ]
        
    # validate kiểm tra xã phường có thuộc quận huyện hay không, quận huyện có thuộc thành phố hay không    
    def validate(self, data):
        province = data.get('province')
        district = data.get('district')
        ward = data.get('ward')

        if district and district.province != province:
            raise serializers.ValidationError("quận huyện không thuộc thành phố.")
        if ward and ward.district != district:
            raise serializers.ValidationError("xã phường không thuộc quận huyện.")
        return data
    
    def create(self, validated_data):
        images = validated_data.pop('images', [])
        homestay = Homestay.objects.create(**validated_data)
        for image in images:
            HomestayImage.objects.create(
                homestay=homestay,
                image_url=image
            )
        return homestay
    
# tạo class HomestayImageSerializer để serialize dữ liệu ảnh của homestay sang json 
class HomestayImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = HomestayImage
        fields = ['id', 'image_url']

class MyHomestaySerializer(serializers.ModelSerializer):

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
# custom serializer field để hiển thị danh sách ảnh của homestay
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
        # Text hiển thị
            'province_name',
            'district_name',
            'ward_name',

            'description',
            'deleted_at',
            'images'
        ]

class UpdateHomestaySerializer(serializers.ModelSerializer):

    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
        )

    class Meta:
        model = Homestay
        fields = [
                'name', 
                'address', 
                'description', 
                'province', 
                'district',
                'ward',
                'images'
                ]
# GIẢI THÍCH ĐOẠN CODE NÀY:        
    def update(self, instance, validated_data):

        images = validated_data.pop('images', None)

        # update thông tin thường
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        # nếu có upload ảnh mới
        if images is not None:
            # xóa ảnh cũ
            instance.images.all().delete()
            # tạo ảnh mới
            for image in images:
                HomestayImage.objects.create(
                    homestay=instance,
                    image_url=image
                )
        return instance


class HomestayDetailSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = Homestay
        fields = [
            'id',
            'name',
            'address',
            'description',

            # FK ID thật
            'province',
            'district',
            'ward',

            # Text hiển thị
            'province_name',
            'district_name',
            'ward_name',
        ]