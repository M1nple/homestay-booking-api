from django.urls import path, include
from rest_framework.routers import DefaultRouter

from homestays.views.public.homestay_views import PublicHomestayViewSet


router = DefaultRouter()

router.register(
    r'homestays',
    PublicHomestayViewSet,
    basename='public-homestay'
)

urlpatterns = [
    path('', include(router.urls)),
]