from rest_framework import serializers
from .models import Room, RoomImage

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
                'homestay',
                'name', 
                'price', 
                'capacity', 
                'status', 
                'description',
                'images'
                ]
        
    def create(self, validated_data):
        images = validated_data.pop('images', [])
        room = Room.objects.create(**validated_data)
        for image in images:
            RoomImage.objects.create(
                room=room,
                image_url=image
            )
        return room
    