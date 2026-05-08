from django.urls import path
from bookings.views.customer_views import BookingViewSet

booking_viewset = BookingViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

urlpatterns = [
    path('bookings/', booking_viewset, name='booking-list-create'),
]