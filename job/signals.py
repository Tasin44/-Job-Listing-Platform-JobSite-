from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from job.models import JobApplication
from authapp.utils import EmailService

@receiver(post_save, sender=JobApplication)
def send_application_notifications(sender, instance, created, **kwargs):

    if created:

        EmailService.send_job_application_notification(instance.job, instance.candidate)
        

        subject = 'Application Submitted Successfully'
        message = f'Hi {instance.candidate.get_full_name()},\n\n' \
                 f'Your application for "{instance.job.title}" has been received.\n\n' \
                 f'We will review your application and get back to you soon.\n\n' \
                 f'Regards,\nJobSite Team'
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.candidate.email],
            fail_silently=False,
        )