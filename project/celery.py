# How to run celery tasks
# You also need to install Celery, Redis and run 4 terminals
# 1 - common to run the Redis server: redis-server (Ctrl-C -> stop)
# 2 - terminal of the project environment: python 3 manage.py runserver
# 3 - project environment terminal for running tasks without a schedule: celeri -A project worker -info --concurrency=10
# where --concurrency is the number of processes that can run on it
# 4 - (optional) project environment terminal for running scheduled tasks: celery -A project beat -l INFO
# where beat m.b. is replaced by the -B flag after INFO
# in addition, installation in the environment and configuration in settings.py

import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('bboard')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'news_week_every_monday_8am': {
#         'task': 'news.tasks.news_week',
#         'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
#         # 'schedule': crontab(), #для отладки
#         # 'args': (agrs),
#     },
# }

