from django.contrib import admin
from .models import Booking, Attendance


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("pet", "start_time", "end_time", "status")


admin.site.register(Attendance)
