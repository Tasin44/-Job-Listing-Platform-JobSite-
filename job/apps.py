
from django.apps import AppConfig

class JobConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'job'
    verbose_name = 'Jobs'

    def ready(self):

        try:
            import job.signals
        except ImportError:
            pass