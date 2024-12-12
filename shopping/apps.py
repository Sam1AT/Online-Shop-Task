from django.apps import AppConfig
import os


class ShoppingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shopping'


    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true':
            from .tasks import start_expiry_listener
            start_expiry_listener()