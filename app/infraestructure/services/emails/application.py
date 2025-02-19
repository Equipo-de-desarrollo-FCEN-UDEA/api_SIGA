from __future__ import annotations

import smtplib
from email.message import EmailMessage

from jinja2 import Environment
from jinja2 import FileSystemLoader

from .templates import templatesdir
from app.core.celery_worker import celery_app
from app.core.config import settings
from app.core.logging import logging

logger = logging.getLogger(__name__)

env = Environment(
    loader=FileSystemLoader(templatesdir),
    autoescape=True,
)

_my_email = settings.smtp_prod_user_email


@celery_app.task
def create_application_email(
    to_name: str,
    to_lastname: str,
    tipo_solicitud: str,
    email: str,
):
    template = env.get_template('email.creacion.solicitud.html.j2')

    context = {
        'user': {'nombre': to_name, 'apellido': to_lastname},
        'req': {'tipo_solicitud': tipo_solicitud},

    }

    render = template.render(context)
    msg = EmailMessage()
    msg['Subject'] = 'Creación de solicitud'
    msg['From'] = _my_email
    msg['To'] = email
    msg.set_content(
        render,
        subtype='html',
    )

    with smtplib.SMTP(
        settings.smtp_local_host_email,
        port=settings.smtp_local_port_email,
    ) as smtp:
        smtp.send_message(
            msg=msg,
            from_addr=_my_email,
            to_addrs=email,
        )


@celery_app.task
def update_status_email(
    tipo_solicitud: str,
    observacion: str,
    nombre_estado: str,
    uuid: str,
    email: list[str] | str,
):
    template = env.get_template('email.cambio.estado.html.j2')
    enlace = f'{settings.APP_DOMAIN}/solicitudes/{tipo_solicitud}/ver/{uuid}'
    context = {
        'req': {
            'tipo_solicitud': tipo_solicitud,
            'observacion': observacion,
            'nombre_estado': nombre_estado,
        },
        'estado': {'nombre_estado': nombre_estado},
        'Enlace': enlace,
    }
    render = template.render(context)
    msg = EmailMessage()
    msg['Subject'] = 'Actualización de estado'
    msg['From'] = _my_email
    msg['To'] = ', '.join(email) if isinstance(email, list) else email
    msg.set_content(
        render,
        subtype='html',
    )
    with smtplib.SMTP(
        settings.smtp_local_host_email,
        port=settings.smtp_local_port_email,
    ) as smtp:
        smtp.send_message(
            msg=msg,
            from_addr=_my_email,
            to_addrs=email,
        )
