from django.db import models
from users.models import User
from homestays.models import Homestay
from rooms.models import Room

class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING'
        CONFIRMED = 'CONFIRMED'
        CANCELLED = 'CANCELLED'
        COMPLETED = 'COMPLETED'
        REJECTED = 'REJECTED'
        PENDING_PAYMENT = 'PENDING_PAYMENT'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    homestay = models.ForeignKey(Homestay, on_delete=models.CASCADE)

    check_in = models.DateField(db_index=True)
    check_out = models.DateField(db_index=True)

    total_guests = models.IntegerField()
    total_price = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, 
                            choices=Status.choices, 
                            default=Status.PENDING,
                            db_index=True
                            )

    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancelled_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='cancelled_bookings')
    cancel_reason = models.TextField(null=True, blank=True)
    confirm_at = models.DateTimeField(null=True, blank=True)
    # rejected_at = models.DateTimeField(null=True, blank=True) theem sau

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BookingRoom(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='booking_rooms')
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        unique_together = ('booking', 'room')