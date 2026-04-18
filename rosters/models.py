from django.db import models
from accounts.models import User


class Shift(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class Timesheet(models.Model):
    shift = models.OneToOneField(Shift, on_delete=models.CASCADE)
    clocked_in = models.DateTimeField(null=True, blank=True)
    clocked_out = models.DateTimeField(null=True, blank=True)
