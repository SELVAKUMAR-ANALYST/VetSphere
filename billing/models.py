from django.db import models
from bookings.models import Booking


class Invoice(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    issued_date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[("unpaid", "Unpaid"), ("paid", "Paid")],
        default="unpaid",
    )


class Payment(models.Model):
    PAYMENT_METHODS = [
        ("cash", "Cash"),
        ("digital", "Digital Payment"),
    ]
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHODS, default="digital"
    )
    payment_date = models.DateTimeField(auto_now_add=True)
