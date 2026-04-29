from django.db import models


# Provinces
class Province(models.Model):
    code = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)

    division_type = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    codename = models.CharField(
        max_length=100,
        unique=True
    )

    phone_code = models.IntegerField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'provinces'
        ordering = ['name']

    def __str__(self):
        return self.name

# Districts
class District(models.Model):
    province = models.ForeignKey(
        Province,
        on_delete=models.CASCADE,
        related_name='districts'
    )

    code = models.IntegerField(unique=True)

    name = models.CharField(max_length=100)

    division_type = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    codename = models.CharField(
        max_length=100,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'districts'
        ordering = ['name']

    def __str__(self):
        return self.name


# Wards
class Ward(models.Model):
    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        related_name='wards'
    )

    code = models.IntegerField(unique=True)

    name = models.CharField(max_length=100)

    division_type = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    codename = models.CharField(
        max_length=100,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'wards'
        ordering = ['name']

    def __str__(self):
        return self.name