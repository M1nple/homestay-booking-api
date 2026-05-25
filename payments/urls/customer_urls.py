from rest_framework.routers import DefaultRouter

from payments.views.customer_views import CustomerPaymentViewSet


router = DefaultRouter()

router.register(
    r'payments',
    CustomerPaymentViewSet,
    basename='customer-payments'
)

urlpatterns = router.urls