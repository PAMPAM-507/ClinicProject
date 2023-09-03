import os

from celery import Celery, schedules
from celery.schedules import schedule
from celery.schedules import crontab
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ClinicProject.settings')

app = Celery('ClinicProject')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    'authForModel': {
        'task': 'ClinicWebsite.tasks.register_to_model',
        # 'schedule': crontab(minute='*/5'),
        'schedule': timedelta(seconds=290),
    },

    'refreshAccessToken': {
        'task': 'ClinicWebsite.tasks.refresh_access_token',
        'schedule': timedelta(seconds=50),
    },
}
