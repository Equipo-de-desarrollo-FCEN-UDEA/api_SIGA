from celery import Celery
from app.core.config import settings

include = [
    "app.infraestructure.services.emails.user"
]

celery_app = Celery('tasks', broker=settings.redis_url, backend=settings.redis_url, include=include)

celery_app.conf.update(task_track_started=True)