from django.shortcuts import render
from rest_framework import generics
from .models import Province, District, Ward
from locations.serializer import ProvinceSerializer, DistrictSerializer, WardSerializer

class ProvinceList(generics.ListAPIView):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer

class DistrictList(generics.ListAPIView):
    serializer_class = DistrictSerializer

    def get_queryset(self):
        province_id = self.request.query_params.get('province_id')
        queryset = District.objects.all()
        if province_id:
            queryset = queryset.filter(province_id=province_id)
        return queryset
    
class WardList(generics.ListAPIView):
    serializer_class = WardSerializer

    def get_queryset(self):
        district_id = self.request.query_params.get('district_id')
        queryset = Ward.objects.all()
        if district_id:
            queryset = queryset.filter(district_id=district_id)
        return queryset