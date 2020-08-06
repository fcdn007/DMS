from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

from .settings import broker_url, TIME_ZONE

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'databaseDemo.settings')

app = Celery('databaseDemo', broker=broker_url)

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


app.conf.beat_schedule = {
    'check_merge_df_newest': {
        "task": "databaseDemo.tasks.keep_merge_df_newest_by_celery",
        "schedule": crontab(minute=0, hour="22"),  # crontab(minute="*/10"),
        "args": (),
    },
    'backup_db': {
        "task": "databaseDemo.tasks.backup_db_by_celery",
        "schedule": crontab(minute=0, hour="22"),  # crontab(minute="*/10"),
        "args": (),
    },
    'clean_media': {
        "task": "databaseDemo.tasks.clean_media_by_celery",
        "schedule": crontab(minute=0, hour="22"),  # crontab(minute="*/10"),
        "args": (),
    },
}
app.conf.timezone = TIME_ZONE
