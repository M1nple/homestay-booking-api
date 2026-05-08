from rest_framework import serializers
from ..models import Room, RoomImage

class CreateRoomSerializer(serializers.ModelSerializer):

    # custom serializer field vì model không có trường images, 
    # nên phải tạo thủ công để lấy dữ liệu ảnh từ model RoomImage thông qua related_name 'images'
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
        )
    
    class Meta:
        model = Room
        fields = [
                'name', 
                'price', 
                'capacity', 
                'status', 
                'description',
                'images'
                ]

    def validate(self, data):
        price = data.get('price')
        capacity = data.get('capacity')

        if price is not None and price < 0:
            raise serializers.ValidationError("Giá phòng phải lớn hơn 0.")
        if capacity is not None and capacity <= 0:
            raise serializers.ValidationError("số khách phải lớn hơn 1.")
        return data   

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        room = Room.objects.create(**validated_data)
        for image in images:
            RoomImage.objects.create(
                room=room,
                image_url=image
            )
        return room
    
class RoomImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomImage
        fields = ['id', 'image_url']

class UpdateRoomSerializer(serializers.ModelSerializer):

    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    class Meta:
        model = Room
        fields = [
                'name', 
                'price', 
                'capacity', 
                'status', 
                'description',
                'images',
                ]

    def validate(self, data):
        price = data.get('price')
        capacity = data.get('capacity')

        if price is not None and price < 0:
            raise serializers.ValidationError("Giá phòng phải lớn hơn 0.")
        if capacity is not None and capacity <= 0:
            raise serializers.ValidationError("số khách phải lớn hơn 1.")
        return data
    
    def update(self, instance, validated_data):

        images = validated_data.pop('images', None) # giải thích  

        #update các trường thông tin của phòng
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        # nếu có upload ảnh mới
        if images is not None:
            # xóa ảnh cũ
            instance.images.all().delete()
            # tạo ảnh mới
            for image in images:
                RoomImage.objects.create(
                    room=instance,
                    image_url=image
                )
        return instance

class RoomListSerializer(serializers.ModelSerializer):
    images = RoomImageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = [
            'id',
            'name',
            'price',
            'capacity',
            'status',
            'description',
            'deleted_at',
            'images'
        ]
    
class RoomDetailSerializer(serializers.ModelSerializer):
    images = RoomImageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = [
            'id',
            'name',
            'price',
            'capacity',
            'status',
            'description',
            'deleted_at',
            'images'
        ]

    
