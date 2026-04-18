from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Booking


@receiver(post_save, sender=Booking)
def notify_booking_status_change(sender, instance, created, **kwargs):
    """
    Sends an email notification when a booking status is updated to 'confirmed'.
    """
    if not created:  # Only for updates
        if instance.status == "confirmed":
            pet_owner = instance.pet.owner
            subject = f"Booking Confirmed for {instance.pet.name}!"
            message = (
                f"Hi {pet_owner.username},\n\n"
                "We are happy to inform you that your booking for "
                f"{instance.pet.name} has been confirmed.\n\n"
                f"Service: {instance.service.name}\n"
                f"Start: {instance.start_time}\n"
                f"End: {instance.end_time}\n\n"
                "Thank you for choosing Pet Care!"
            )

            send_mail(
                subject,
                message,
                "support@petcare.com",
                [pet_owner.email],
                fail_silently=True,
            )
            print(
                f"DEBUG: Email sent to {pet_owner.email} for confirmed booking."
            )
