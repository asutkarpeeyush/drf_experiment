import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drf_experiment.settings")
app = Celery("drf_experiment")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()