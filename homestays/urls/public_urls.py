from django.urls import path, include
from rest_framework.routers import DefaultRouter

from homestays.views.public.homestay_views import PublicHomestayViewSet


public_router = DefaultRouter()

public_router.register(
    r'homestays',
    PublicHomestayViewSet,
    basename='public-homestay'
)

urlpatterns = [
    path('', include(public_router.urls)),
]