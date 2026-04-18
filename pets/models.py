from django.db import models
from accounts.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone


class Pet(models.Model):
    PET_TYPE_CHOICES = [
        ("dog", "Dog"),
        ("cat", "Cat"),
        ("bird", "Bird"),
        ("rabbit", "Rabbit"),
        ("hamster", "Hamster"),
        ("fish", "Fish"),
        ("other", "Other"),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    pet_type = models.CharField(
        max_length=20, choices=PET_TYPE_CHOICES, default="dog"
    )
    breed = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(0)])
    medical_info = models.TextField(blank=True)
    image = models.ImageField(upload_to="pet_photos/", blank=True, null=True)




class DailyLog(models.Model):
    ACTIVITY_CHOICES = [
        ("feeding", "Feeding"),
        ("walk", "Walk"),
        ("medication", "Medication"),
        ("grooming", "Grooming"),
        ("behavior", "Behavior"),
        ("other", "Other"),
    ]
    pet = models.ForeignKey(
        Pet, on_delete=models.CASCADE, related_name="daily_logs"
    )
    date = models.DateTimeField(auto_now_add=True)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_CHOICES)
    notes = models.TextField()
    logged_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ["-date"]


class VaccinationRecord(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    expiry_date = models.DateField()


class HealthLog(models.Model):
    LOG_TYPE_CHOICES = [
        ("checkup", "Regular Checkup"),
        ("vaccination", "Vaccination"),
        ("surgery", "Surgery"),
        ("medication", "Medication Start"),
        ("emergency", "Emergency"),
        ("other", "Other"),
    ]
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="health_logs")
    log_type = models.CharField(max_length=20, choices=LOG_TYPE_CHOICES, default="checkup")
    date = models.DateField(default=timezone.now)
    description = models.TextField()
    veterinarian_name = models.CharField(max_length=100, blank=True)
    follow_up_required = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.log_type} for {self.pet.name} on {self.date}"
