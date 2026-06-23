from django.db import models
from bookings.models import Booking

# =====================
# Payments
# =====================
class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING'
        SUCCESS = 'SUCCESS'
        FAILED = 'FAILED'
        REFUNDED ='REFUNDED'
    class Method(models.TextChoices):
        VNPAY = 'VNPAY'
        MOMO = 'MOMO'
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    method = models.CharField(max_length=20, choices=Method.choices)
    status = models.CharField(max_length=20, 
                              choices=Status.choices, 
                              default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PaymentAttempt(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='attempts')
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    status = models.CharField(max_length=20, choices=Payment.Status.choices)

    txn_ref = models.CharField(max_length=100, unique=True)
    vnp_transaction_no = models.CharField(max_length=100, blank=True, null=True)
    vnp_response_code = models.CharField(max_length=10, blank=True, null=True)
    bank_code = models.CharField(max_length=20, blank=True, null=True)
    pay_date = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)