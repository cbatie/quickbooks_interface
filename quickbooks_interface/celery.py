import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quickbooks_interface.settings')

app = Celery('quickbooks_interface')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
