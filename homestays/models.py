from django.db import models
from locations.models import Province, District, Ward
from users.models import User

class Homestay(models.Model):
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='homestays'
        )
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    province = models.ForeignKey(
        Province,
        on_delete=models.PROTECT, #PROTECT sẽ không cho xóa nếu dữ liệu trường này đang được sử dụng
        related_name='homestays'
    )
    district = models.ForeignKey(
        District,
        on_delete=models.PROTECT,
        related_name='homestays'
    )
    ward = models.ForeignKey(
        Ward,
        on_delete=models.PROTECT,
        related_name='homestays'
    )
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

