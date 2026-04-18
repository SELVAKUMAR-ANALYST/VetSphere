from django.contrib import admin
from .models import User, StaffProfile, CustomerProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_staff_member", "is_customer")


admin.site.register(StaffProfile)
admin.site.register(CustomerProfile)
