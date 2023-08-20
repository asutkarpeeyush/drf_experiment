from django.apps import AppConfig
from django.core.signals import request_finished

class DrfConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'drf'

    # def ready(self):
    #     from . import signals
    #     request_finished.connect(signals.a_simple_signal)