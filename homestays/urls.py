from django.urls import path, include
from .views.host.homestay_views import HomestayViewSet
from rest_framework.routers import DefaultRouter



# Cấu hình host routes
host_router = DefaultRouter()
host_router.register(r'homestays', HomestayViewSet, basename='host-homestay')

urlpatterns = [
    # Đường dẫn cho host quản lý homestay
    path('host/', include(host_router.urls)),
]