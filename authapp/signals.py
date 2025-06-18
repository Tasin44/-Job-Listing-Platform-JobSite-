from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings


from core.models import User

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):

    if created and instance.email:
        subject = 'Welcome to JobSite Platform!'
        message = f'Hi {instance.get_full_name() or instance.username},\n\n' \
                 f'Welcome to JobSite! Your account has been successfully created.\n\n' \
                 f'Regards,\nJobSite Team'
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
        )

