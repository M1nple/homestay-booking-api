from rest_framework import serializers
from .models import Homestay

class HomestaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Homestay
        fields = [
                'name', 
                'address', 
                'description', 
                'price_per_night', 
                'province', 
                'district',
                'ward',
                ]
        
    # validate kiểm tra xã phường có thuộc quận huyện hay không, quận huyện có thuộc thành phố hay không    
    def validate(self, data):
        province = data.get('province')
        district = data.get('district')
        ward = data.get('ward')

        if district and district.province != province:
            raise serializers.ValidationError("quận huyện không thuộc thành phố.")
        if ward and ward.district != district:
            raise serializers.ValidationError("xã phường không thuộc quận huyện.")
        return data