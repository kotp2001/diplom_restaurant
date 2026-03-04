from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'table', 'guest_name', 'guest_phone', 'booking_date', 'booking_time', 'guests_count']
    list_filter = ['booking_date', 'table']
    search_fields = ['guest_name', 'guest_phone']
    date_hierarchy = 'booking_date'