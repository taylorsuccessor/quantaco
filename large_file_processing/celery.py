import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apidjango.settings")

app = Celery("large_file_processing")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
