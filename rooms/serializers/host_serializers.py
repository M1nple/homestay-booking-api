from rest_framework import serializers
from django.db.models import Avg
from rooms.serializers.amenity_serializers import AmenitySerializer
from ..models import Room, RoomImage, Amenity


class CreateRoomSerializer(serializers.ModelSerializer):

    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    amenity_ids = serializers.PrimaryKeyRelatedField(
        queryset= Amenity.objects.all(),
        many=True,
        write_only=True,
        source='amenities'
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
            'amenity_ids'
        ]

    def validate(self, data):

        price = data.get('price')
        capacity = data.get('capacity')

        if price is not None and price < 0:
            raise serializers.ValidationError(
                "Giá phòng phải lớn hơn 0."
            )

        if capacity is not None and capacity <= 0:
            raise serializers.ValidationError(
                "Số khách phải lớn hơn 0."
            )

        return data

    def create(self, validated_data):

        images = validated_data.pop('images', [])

        amenities = validated_data.pop('amenities', [])

        room = Room.objects.create(**validated_data)

        room.amenities.set(amenities)

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

    amenity_ids = serializers.PrimaryKeyRelatedField(
        queryset= Amenity.objects.all(),
        many=True,
        write_only=True,
        source='amenities'
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
                'amenity_ids',
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

        images = validated_data.pop('images', None)

        amenities = validated_data.pop(
            'amenities',
            None
        )

        # update field thường
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # update many-to-many
        if amenities is not None:
            instance.amenities.set(amenities)

        # update ảnh
        if images is not None:

            instance.images.all().delete()

            for image in images:

                RoomImage.objects.create(
                    room=instance,
                    image_url=image
                )

        return instance

class RoomListSerializer(serializers.ModelSerializer):
    images = RoomImageSerializer(many=True, read_only=True)

    amenities = AmenitySerializer(
        many=True,
        read_only=True
    )

    avg_rating = serializers.SerializerMethodField()
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
            'images',
            'amenities',
            'avg_rating',
        ]
    def get_avg_rating(self, obj):

        return obj.reviews.aggregate(
            avg=Avg('rating')
        )['avg']
    
class RoomDetailSerializer(serializers.ModelSerializer):
    images = RoomImageSerializer(many=True, read_only=True)
    amenities = AmenitySerializer(
        many=True,
        read_only=True
    )
    avg_rating = serializers.SerializerMethodField()

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
            'images',
            'amenities',
            'avg_rating',
        ]

    def get_avg_rating(self, obj):

        return obj.reviews.aggregate(
            avg=Avg('rating')
        )['avg']
