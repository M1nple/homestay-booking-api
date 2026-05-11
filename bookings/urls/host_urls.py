from rest_framework.routers import DefaultRouter

from bookings.views.host_views import HostBookingViewSet

router = DefaultRouter()
router.register(
    r'bookings',
    HostBookingViewSet,
    basename='host-booking'
)
urlpatterns = router.urls