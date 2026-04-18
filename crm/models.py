from django.db import models


class Enquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("new", "New"),
            ("contacted", "Contacted"),
            ("converted", "Converted"),
        ],
        default="new",
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Waitlist(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    added_at = models.DateTimeField(auto_now_add=True)


class EmailTemplate(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    body = models.TextField()
