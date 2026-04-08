from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_staff_member = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)


class StaffProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="staff_profile"
    )
    pay_rate = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    emergency_contact = models.CharField(max_length=100, blank=True)


class CustomerProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="customer_profile"
    )
    billing_address = models.TextField(blank=True)
    bond_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
