from django.db import models
from django.core.validators import (MinValueValidator,MaxValueValidator)
from users.models import User
from rooms.models import Room
from bookings.models import Booking
from cloudinary_storage.storage import MediaCloudinaryStorage



# =====================
# Review
# =====================

class Review(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    comment = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        unique_together = (
            'user',
            'room',
            'booking'
        )

        ordering = ['-created_at']

    def __str__(self):

        return (
            f'{self.user.email} '
            f'- {self.room.name} '
            f'- {self.rating}'
        )


# =====================
# Review Image
# =====================

class ReviewImage(models.Model):

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image_url = models.ImageField(
        upload_to='reviews/', storage=MediaCloudinaryStorage(),blank=True,null=True)

    created_at = models.DateTimeField(
        auto_now_add=True
    )
