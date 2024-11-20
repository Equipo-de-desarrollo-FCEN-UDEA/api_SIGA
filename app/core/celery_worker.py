from celery import Celery
from app.core.config import settings

include = [
    "app.infraestructure.services.email"
]

celery_app = Celery('tasks', broker=settings.redis_url, backend=settings.redis_url, include=include)

celery_app.conf.update(
    result_expires=3600,
)

@celery_app.task
def send_activation_email(user_email):
    # Lógica para enviar correo de activación
    print(f"Sending activation email to {user_email}")