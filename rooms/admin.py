from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Room 

class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'capacity', 'status', 'homestay', 'deleted_at']
    list_filter = ['status', 'homestay']
    search_fields = ['name', 'description']

    fieldsets = (
        (None, {'fields': ('name', 'price', 'capacity', 'status', 'description', 'homestay', 'deleted_at')}),
    )   

admin.site.register(Room, RoomAdmin)