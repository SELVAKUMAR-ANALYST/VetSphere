from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Invoice


@receiver(post_save, sender=Invoice)
def notify_new_invoice(sender, instance, created, **kwargs):
    """
    Sends an email notification when a new invoice is generated.
    """
    if created:
        pet_owner = instance.booking.pet.owner
        subject = f"New Invoice for {instance.booking.pet.name}"
        message = (
            f"Hi {pet_owner.username},\n\n"
            "A new invoice has been generated for your pet's stay.\n\n"
            f"Amount: ${instance.amount}\n"
            f"Date: {instance.issued_date}\n\n"
            "You can view and pay your invoice on your dashboard."
        )

        send_mail(
            subject,
            message,
            "billing@petcare.com",
            [pet_owner.email],
            fail_silently=True,
        )
        print(
            f"DEBUG: Billing email sent to {pet_owner.email} for invoice #{instance.id}."
        )
