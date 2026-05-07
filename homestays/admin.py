from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Homestay

class HomestayAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'owner', 'province', 'district', 'ward', 'deleted_at']
    list_filter = ['deleted_at']
    search_fields = ['name','province', 'district', 'ward']

    fieldsets = (
        (None, {'fields': ('name', 'description', 'province', 'district', 'ward', 'owner', 'deleted_at')}),
    )

admin.site.register(Homestay, HomestayAdmin)