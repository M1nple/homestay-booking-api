from django.db import models
from homestays.models import Homestay
from cloudinary_storage.storage import MediaCloudinaryStorage


# Create your models here.
# =====================
# Rooms
# =====================
class Room(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'AVAILABLE'
        MAINTENANCE = 'MAINTENANCE'

    homestay = models.ForeignKey(Homestay, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=15, decimal_places=2, db_index=True)
    capacity = models.IntegerField()
    status = models.CharField(max_length=20, choices=Status.choices, db_index=True)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    def __str__(self):  
        return self.name


class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images')
    image_url = models.ImageField(upload_to='room_images/', storage=MediaCloudinaryStorage(), blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)