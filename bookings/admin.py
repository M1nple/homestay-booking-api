from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Booking
# Register your models here.

class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'homestay', 'check_in', 'check_out', 'total_guests', 'total_price', 'status']

admin.site.register(Booking, BookingAdmin)
