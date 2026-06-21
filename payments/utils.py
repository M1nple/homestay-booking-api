import hmac
import hashlib
import urllib.parse
import pytz
from datetime import timedelta

from django.conf import settings
from django.utils import timezone


def create_vnpay_payment_url(request, payment_attempt):

    vn_timezone = pytz.timezone('Asia/Ho_Chi_Minh')

    current_time = timezone.now().astimezone(
        vn_timezone
    )

    params = {
        'vnp_Version': '2.1.0',
        'vnp_Command': 'pay',
        'vnp_TmnCode': settings.VNPAY_TMN_CODE,
        'vnp_Amount': int(payment_attempt.amount * 100),
        'vnp_CurrCode': 'VND',
        'vnp_TxnRef': payment_attempt.txn_ref,
        'vnp_OrderInfo': (
            f'Thanh toan booking '
            f'{payment_attempt.payment.booking.id}'
        ),
        'vnp_OrderType': 'billpayment',
        'vnp_Locale': 'vn',
        'vnp_ReturnUrl': settings.VNPAY_RETURN_URL,
        'vnp_IpAddr': get_client_ip(request),
        'vnp_CreateDate': current_time.strftime(
            '%Y%m%d%H%M%S'
        ),
        'vnp_ExpireDate': (
            current_time + timedelta(minutes=15)
        ).strftime('%Y%m%d%H%M%S'),
    }

    sorted_params = sorted(params.items())

    query_string = urllib.parse.urlencode(sorted_params)

    hash_value = hmac.new(
        settings.VNPAY_HASH_SECRET_KEY.encode(),
        query_string.encode(),
        hashlib.sha512
    ).hexdigest()

    payment_url = (
        f"{settings.VNPAY_PAYMENT_URL}"
        f"?{query_string}&vnp_SecureHash={hash_value}"
    )

    return payment_url


def get_client_ip(request):

    x_forwarded_for = request.META.get(
        'HTTP_X_FORWARDED_FOR'
    )

    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]

    return request.META.get('REMOTE_ADDR')