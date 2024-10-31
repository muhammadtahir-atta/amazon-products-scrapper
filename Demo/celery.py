from celery import Celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Demo.settings")

app = Celery("Demo")
app.config_from_object("django.conf:settings", namespace="CELERY")
# app.autodiscover_tasks()
app.autodiscover_tasks(['scraper'])
