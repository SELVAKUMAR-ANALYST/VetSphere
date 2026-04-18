from django.contrib import admin
from .models import Shift, Timesheet


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ("staff", "start_time", "end_time")


admin.site.register(Timesheet)
