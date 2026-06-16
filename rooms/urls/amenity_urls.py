from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rooms.views.amenity_views import AmenityViewSet


router = DefaultRouter()

router.register(
    r'amenities',
    AmenityViewSet,
    basename='amenity'
)

urlpatterns = [
    path('', include(router.urls)),
]