from rest_framework import serializers
from ..models import Room, RoomImage
from django.db.models import Avg

class RoomImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomImage
        fields = ['id', 'image_url']

class PublicRoomSerializer(serializers.ModelSerializer):
    images = RoomImageSerializer(many=True, read_only=True)
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = [
            'id',
            'name',
            'price',
            'capacity',
            'description',
            'images',
            'homestay',
            'avg_rating',
        ]
    def get_avg_rating(self, obj):

        return obj.reviews.aggregate(
            avg=Avg('rating')
        )['avg']