
from django.urls import path
from ..views.host_views import HostPaymentView

urlpatterns = [
    path(
        'payments/',
        HostPaymentView.as_view()
    ),
]