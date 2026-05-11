from django.urls import path
from bookings.views.customer_views import CustomerBookingViewSet
from rest_framework.routers import DefaultRouter

# booking_viewset = CustomerBookingViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
    
# urlpatterns = [
#     path('bookings/', booking_viewset, name='booking-list-create'),
# ]


router = DefaultRouter()

router.register(
    r'bookings',
    CustomerBookingViewSet,
    basename='customer-booking'
)

urlpatterns = router.urls