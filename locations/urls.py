from django.urls import path
from .views import ProvinceList, DistrictList, WardList

urlpatterns = [
    path('provinces/', ProvinceList.as_view(), name='province-list'),
    path('districts/', DistrictList.as_view(), name='district-list'),
    path('wards/', WardList.as_view(), name='ward-list'),
]