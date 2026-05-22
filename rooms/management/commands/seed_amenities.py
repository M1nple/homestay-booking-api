from django.core.management.base import BaseCommand

from rooms.models import Amenity


class Command(BaseCommand):

    help = 'Seed amenities data'

    def handle(self, *args, **kwargs):

        amenities = [
            'Wifi',
            'Điều hòa',
            'TV',
            'Phòng bếp', 
            'Máy giặt',
            'Bãi đậu xe',
            'Hồ bơi',
            'Máy sấy quần áo',
            'Nước nóng',
            'Tủ lạnh',
            'Máy sấy tóc',
            'Không gian làm việc',
            'Ban công',
            'Cho phép mang theo thú cưng',
            'Cho phép hút thuốc',
            'Khu vưc nướng BBQ',
            'Camara an ninh',
            'Bình chữa cháy',
            'Lò vi sóng',
            'Bàn ủi',
            'Bàn là',
        ]

        created_count = 0

        for amenity_name in amenities:

            _, created = Amenity.objects.get_or_create(
                name=amenity_name
            )

            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Seeded {created_count} amenities successfully.'
            )
        )