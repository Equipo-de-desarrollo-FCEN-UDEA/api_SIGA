from __future__ import annotations

from celery import Celery
from celery.schedules import crontab

from app.core.config import settings

include = [
    'app.infraestructure.services.emails.user',
    'app.core.tasks',
]

celery_app = Celery(
    'tasks', broker=settings.redis_url,
    backend=settings.redis_url, include=include,
)

celery_app.conf.update(task_track_started=True)

celery_app.conf.beat_schedule = {
    'send-scheduled-emails': {
        'task': 'app.core.tasks.check_expired_commissions',
        'schedule': crontab(hour=5, minute=0),  # Todos los días a las 5:00 AM
    },
}
