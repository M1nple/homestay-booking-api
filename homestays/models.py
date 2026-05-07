from django.db import models
from locations.models import Province, District, Ward
from users.models import User
from cloudinary_storage.storage import MediaCloudinaryStorage


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

    def __str__(self):
        return self.name

class HomestayImage(models.Model):
    homestay = models.ForeignKey(Homestay, on_delete=models.CASCADE, related_name='images')
    image_url = models.ImageField(upload_to='homestay_images/',
                                    storage=MediaCloudinaryStorage(),
                                    blank=True,
                                    null=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)