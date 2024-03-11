from django.apps import AppConfig


class EcomappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'EcomApp'

    def ready(self):
        import EcomApp.signals