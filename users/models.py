from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from cloudinary_storage.storage import MediaCloudinaryStorage

# =====================
# User Manager
# =====================
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # hash password
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ADMIN')

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, password, **extra_fields)


# =====================
# Custom User
# =====================
class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = 'CUSTOMER'
        HOST = 'HOST'
        ADMIN = 'ADMIN'

    # xóa trường username mặc định của AbstractUser và thay thế bằng email làm trường đăng nhập chính
    username = None

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.CUSTOMER
    )

    avatar_url = models.ImageField( upload_to='avatars/',
                                    storage=MediaCloudinaryStorage(),
                                    blank=True, 
                                    null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


# =====================
# Host
# =====================

class HostRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING'
        APPROVED = 'APPROVED'
        REJECTED = 'REJECTED'
        CANCELLED = 'CANCELLED'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Status.choices, default= Status.PENDING, db_index=True)

    business_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    identity_number = models.CharField(max_length=12)
    identity_image = models.ImageField( upload_to='identity_images/',
                                        storage=MediaCloudinaryStorage(),
                                        blank=True, 
                                        null=True)
    reason = models.TextField(blank=True, null=True)

    reviewed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='reviewed_requests')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_name


class HostProfile(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING'
        ACTIVE = 'ACTIVE'
        SUSPENDED = 'SUSPENDED'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    avatar_url = models.URLField(blank=True, null=True)
    identity_number = models.CharField(max_length=100, blank=True, null=True)
    identity_image = models.URLField(blank=True, null=True)

    tax_code = models.CharField(max_length=50, blank=True, null=True)
    bank_account = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    account_holder_name = models.CharField(max_length=255)

    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=Status.choices)

    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='approved_hosts')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)