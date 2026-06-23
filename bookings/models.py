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
        REFUND_PENDING = 'REFUND_PENDING'
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    homestay = models.ForeignKey(Homestay, on_delete=models.CASCADE)
    check_in = models.DateField(db_index=True)
    check_out = models.DateField(db_index=True)
    total_guests = models.IntegerField()
    total_price = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, 
                            choices=Status.choices, 
                            default=Status.PENDING,
                            db_index=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancelled_by = models.ForeignKey(User, 
                                     null=True, 
                                     blank=True, 
                                     on_delete=models.SET_NULL, 
                                     related_name='cancelled_bookings')
    request_refund_at = models.DateField(null=True, blank=True)
    request_refund_by = models.ForeignKey(User, 
                                     null=True, 
                                     blank=True, 
                                     on_delete=models.SET_NULL, 
                                     related_name='request_refund')
    refund_at = models.DateField(null=True, blank=True)
    cancel_reason = models.TextField(null=True, blank=True)
    confirm_at = models.DateTimeField(null=True, blank=True)
    # rejected_at = models.DateTimeField(null=True, blank=True) theem sau
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expired_at = models.DateTimeField(
                                    null=True,
                                    blank=True,
                                    db_index=True)


class BookingRoom(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='rooms')
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        unique_together = ('booking', 'room')