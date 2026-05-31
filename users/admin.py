from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, HostRequest, HostProfile


class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['email', 'full_name', 'role', 'is_staff', 'is_active', 'is_verified']
    list_filter = ['role', 'is_staff', 'is_active']

    search_fields = ['email', 'full_name', 'phone']

    # Hiển thị khi xem detail
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Thông tin cá nhân', {'fields': ('full_name', 'phone', 'avatar_url')}),
        ('Phân quyền', {'fields': ('role', 'is_staff', 'is_superuser', 'is_active', 'is_verified')}),
        ('Thời gian', {'fields': ('last_login',)}),
    )

    # Hiển thị khi tạo user trong admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    filter_horizontal = ()


admin.site.register(User, UserAdmin)

class HostRequestAdmin(admin.ModelAdmin):
    list_display = ['id','business_name', 'user', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['user__email', 'user__full_name']

admin.site.register(HostRequest, HostRequestAdmin)
