from django.contrib import admin
from .models import Pet, VaccinationRecord


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "breed", "age")


admin.site.register(VaccinationRecord)
