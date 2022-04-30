from __future__ import absolute_import, unicode_literals
from celery import Celery
import os
from django.conf import settings
from celery.schedules import crontab
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ETFsavings.settings')

# Create default Celery app
app = Celery('ETFsavings')

app.conf.enable_utc = False

app.conf.update(timezone = 'Europe/Zurich')

# namespace='CELERY' means all celery-related configuration keys
# should be uppercased and have a `CELERY_` prefix in Django settings.
# https://docs.celeryproject.org/en/stable/userguide/configuration.html
app.config_from_object(settings, namespace="CELERY")

#CELERY BEAT Settings

app.conf.beat_schedule = {
      'invest-every-month': {
        'task': 'implementation.tasks.invest',
        'schedule': crontab(day_of_month=25, hour=10, minute=0),
        'args': (500,)
    },
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')