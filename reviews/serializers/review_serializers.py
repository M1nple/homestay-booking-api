from rest_framework import serializers

from reviews.models import (
    Review,
    ReviewImage
)

from bookings.models import (
    Booking,
    BookingRoom
)


class ReviewImageSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = ReviewImage

        fields = [
            'id',
            'image_url'
        ]


class ReviewSerializer(
    serializers.ModelSerializer
):

    user_name = serializers.CharField(
        source='user.username',
        read_only=True
    )

    images = ReviewImageSerializer(
        many=True,
        read_only=True
    )

    class Meta:

        model = Review

        fields = [
            'id',
            'user_name',
            'rating',
            'comment',
            'images',
            'created_at'
        ]


class CreateReviewSerializer(
    serializers.ModelSerializer
):

    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    class Meta:

        model = Review

        fields = [
            'booking',
            'room',
            'rating',
            'comment',
            'images'
        ]

    def validate(self, data):

        request = self.context['request']

        booking = data['booking']

        room = data['room']

        # booking owner
        if booking.user != request.user:

            raise serializers.ValidationError(
                'Không thể review booking này.'
            )

        # booking completed
        if booking.status != Booking.Status.COMPLETED:

            raise serializers.ValidationError(
                'Chỉ được review sau khi hoàn thành.'
            )

        # room thuộc booking
        room_exists = BookingRoom.objects.filter(
            booking=booking,
            room=room
        ).exists()

        if not room_exists:

            raise serializers.ValidationError(
                'Room không thuộc booking.'
            )

        return data

    def create(self, validated_data):

        images = validated_data.pop(
            'images',
            []
        )

        review = Review.objects.create(
            user=self.context['request'].user,
            **validated_data
        )

        for image in images:

            ReviewImage.objects.create(
                review=review,
                image_url=image
            )

        return review