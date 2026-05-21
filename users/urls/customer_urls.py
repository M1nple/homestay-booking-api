from django.urls import path

from users.views.customer_views import HostRequestView

urlpatterns = [
    path(
        'host-requests/',
        HostRequestView.as_view(),
        name='host-requests'
    ),
]