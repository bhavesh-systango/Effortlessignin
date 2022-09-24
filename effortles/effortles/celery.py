from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'effortles.settings')
app = Celery('effortles')

app.config_from_object('django.conf:settings')
app.conf.enable_utc = False
app.conf.update(time="Asia/Kolkata")
app.config_from_object(settings, namespace="CELERY")

app.autodiscover_tasks()


app.conf.beat_schedule={

}
