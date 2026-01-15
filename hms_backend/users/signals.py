from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from .utils import send_email_async

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        print(f"New user created: {instance.username}, sending welcome email...")
        email_data = {
            "name": instance.username,
            "role": "Doctor" if instance.is_doctor else "Patient"
        }
        send_email_async("WELCOME", instance.email, email_data)
