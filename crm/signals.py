from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Enquiry
from django.conf import settings


@receiver(post_save, sender=Enquiry)
def notify_admin_new_enquiry(sender, instance, created, **kwargs):
    """
    Sends an email notification to the admin when a new enquiry is received.
    """
    if created:
        subject = f"New Enquiry from {instance.name}"
        message = (
            "A new enquiry has been received:\n\n"
            f"From: {instance.name}\n"
            f"Email: {instance.email}\n"
            f"Status: {instance.status}\n\n"
            "Please check the CRM admin panel to respond."
        )

        # In a real app, this would go to a staff email.
        # For the viva, we'll print it to self and admin.
        send_mail(
            subject,
            message,
            "system@petcare.com",
            [settings.DEFAULT_FROM_EMAIL],
            fail_silently=True,
        )
        print(
            f"DEBUG: Admin notification sent for enquiry from {instance.name}."
        )
