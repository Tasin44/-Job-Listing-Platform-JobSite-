
import secrets
import string
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


def generate_password_reset_token():

    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(32))

def send_password_reset_email(user, reset_token):

    try:
        subject = 'Password Reset - JobSite Platform'
        
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
    
        reset_link = f"http://127.0.0.1:8000/api/v1/auth/reset-password/?uid={uid}&token={token}"

        html_message = render_to_string('emails/password_reset_email.html', {
            'user': user,
            'reset_link': reset_link,
            'site_name': 'JobSite',
        })
        
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending password reset email: {str(e)}")
        return False



class EmailService:

    @staticmethod
    def send_welcome_email(user):
        if not user.email:
            return  
        subject = 'Welcome to Our Platform'
        message = f'Hello {user.get_full_name()},\n\nThank you for registering!'
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
    @staticmethod
    def send_password_reset_email(user, reset_token):

        return send_password_reset_email(user, reset_token)
    
    @staticmethod
    def send_job_application_notification(job, candidate):

        try:
            subject = f'New Application for {job.title}'
            
            html_message = render_to_string('emails/job_application_notification.html', {
                'job': job,
                'candidate': candidate,
                'recruiter': job.recruiter,
            })
            
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[job.recruiter.email],
                html_message=html_message,
                fail_silently=False,
            )
            return True
        except Exception as e:
            print(f"Error sending job application notification: {str(e)}")
            return False