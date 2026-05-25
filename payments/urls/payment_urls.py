from django.urls import path
from ..views.payment_views import CreateVNPayPaymentView, VNPayReturnView

urlpatterns = [
    path(
        'vnpay/create/<int:booking_id>/',
        CreateVNPayPaymentView.as_view()
    ),

    path(
        'vnpay-return/',
        VNPayReturnView.as_view()
    ),
]