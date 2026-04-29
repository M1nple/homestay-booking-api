import requests
from django.core.management.base import BaseCommand
from locations.models import Province, District, Ward


class Command(BaseCommand):
    help = "Seed Vietnam locations data"
    def handle(self, *args, **kwargs):
        url = "https://provinces.open-api.vn/api/v1/?depth=3"
        self.stdout.write(
            self.style.WARNING("Fetching locations data...")
        )
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
        except requests.RequestException as error:
            self.stdout.write(
                self.style.ERROR(
                    f"API request failed: {error}"
                )
            )
            return
        data = response.json()
        province_count = 0
        district_count = 0
        ward_count = 0
        for province_data in data:
            province, created = Province.objects.get_or_create(
                code=province_data["code"],
                defaults={
                    "name": province_data["name"],
                    "division_type": province_data.get("division_type"),
                    "codename": province_data.get("codename"),
                    "phone_code": province_data.get("phone_code"),
                }
            )
            if created:
                province_count += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f"Province: {province.name}"
                )
            )

            for district_data in province_data.get("districts", []):

                district, created = District.objects.get_or_create(
                    code=district_data["code"],
                    defaults={
                        "province": province,
                        "name": district_data["name"],
                        "division_type": district_data.get("division_type"),
                        "codename": district_data.get("codename"),
                    }
                )

                if created:
                    district_count += 1

                for ward_data in district_data.get("wards", []):
                    _, created = Ward.objects.get_or_create(
                        code=ward_data["code"],
                        defaults={
                            "district": district,
                            "name": ward_data["name"],
                            "division_type": ward_data.get("division_type"),
                            "codename": ward_data.get("codename"),
                        }
                    )

                    if created:
                        ward_count += 1

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Seed completed successfully!\n"
                f"Provinces created: {province_count}\n"
                f"Districts created: {district_count}\n"
                f"Wards created: {ward_count}"
            )
        )
