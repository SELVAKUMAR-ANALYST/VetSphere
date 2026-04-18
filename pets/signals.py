from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import DailyLog


@receiver(post_save, sender=DailyLog)
def notify_daily_log_update(sender, instance, created, **kwargs):
    """
    Sends an email notification when a new daily log is created for a pet.
    """
    if created:
        pet_owner = instance.pet.owner
        subject = f"New Daily Log for {instance.pet.name}!"
        message = (
            f"Hi {pet_owner.username},\n\n"
            f"A new activity has been logged for {instance.pet.name}:\n\n"
            f"Activity: {instance.get_activity_type_display()}\n"
            f"Notes: {instance.notes}\n\n"
            "Check the dashboard for more details."
        )

        send_mail(
            subject,
            message,
            "log-updates@petcare.com",
            [pet_owner.email],
            fail_silently=True,
        )
        print(f"DEBUG: Email sent to {pet_owner.email} for new DailyLog.")
