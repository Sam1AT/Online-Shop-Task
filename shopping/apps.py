from django.apps import AppConfig

from .tasks import start_expiry_listener


class ShoppingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shopping'

    def ready(self):
        start_expiry_listener()
