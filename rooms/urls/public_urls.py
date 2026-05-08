from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rooms.views.public_views import PublicRoomViewSet


router = DefaultRouter()

router.register(
    r'rooms',
    PublicRoomViewSet,
    basename='public-room'
)

urlpatterns = [
    path('', include(router.urls)),
]