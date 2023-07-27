from django.apps import AppConfig


class PushschedulerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pushscheduler'
    def ready(self):
        from .scheduler import start
        start()