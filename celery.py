import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

app = Celery('your_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Schedule the anomaly detection task to run hourly
app.conf.beat_schedule = {
    'detect-suspicious-ips-hourly': {
        'task': 'ip_tracking.tasks.detect_suspicious_ips',
        'schedule': 3600.0,  # Every hour
    },
    'cleanup-old-logs-daily': {
        'task': 'ip_tracking.tasks.cleanup_old_logs',
        'schedule': 86400.0,  # Every day
    },
}