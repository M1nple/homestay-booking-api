import random

from datetime import timedelta

from django.utils import timezone
from django.core.mail import send_mail

from users.models import EmailOTP
from django.conf import settings


def generate_and_send_otp(user):

    EmailOTP.objects.filter(
        user=user,
        is_used=False
    ).delete()

    otp = str(
        random.randint(100000, 999999)
    )
    EmailOTP.objects.create(
        user=user,
        otp_code=otp,
        expired_at=(
            timezone.now()
            + timedelta(minutes=5)
        )
    )
    send_mail(
        subject='Verify Email',
        message=(
            f'Xin chào {user.full_name},\n\n'
            f'Mã OTP của bạn là: {otp}\n\n'
            f'OTP có hiệu lực trong 5 phút.'
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False
    )