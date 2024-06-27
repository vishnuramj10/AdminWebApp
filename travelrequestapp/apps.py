from django.apps import AppConfig
from django.db.models.signals import post_migrate

class TravelappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "travelrequestapp"

    def ready(self):
        import travelrequestapp.signals
