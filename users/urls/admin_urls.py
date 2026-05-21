from rest_framework.routers import DefaultRouter

from django.urls import path
 
from users.views.admin_views import HostRequestViewSet

# list_host_request = HostRequestViewSet.as_view({
#     'get': 'list',
# })

# urlpatterns = [
#     path('host-requests/', list_host_request, name='list-host-request'),
# ]

router = DefaultRouter()
router.register(r'host-requests', HostRequestViewSet, basename='host-requests')

urlpatterns = router.urls