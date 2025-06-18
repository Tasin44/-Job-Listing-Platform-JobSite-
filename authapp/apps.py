from django.apps import AppConfig

class AuthConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authapp'  
    verbose_name = 'Authentication'

    def ready(self):

        import authapp.signals