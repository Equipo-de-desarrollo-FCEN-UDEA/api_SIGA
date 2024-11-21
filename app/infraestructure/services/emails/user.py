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


_my_email = settings.smtp_user_email

_my_pwd = settings.smtp_user_password._secret_value


@celery_app.task
def confirm_email(to_name: str, token: str, email):
    template = env.get_template('email.validar.email.html.j2')
    link = f'{settings.APP_DOMAIN}/auth/activate-account/{token}'
    context = {
        'user': {'nombre': to_name.title()},
        'enlace': link,
    }

    render = template.render(context)
    msg = EmailMessage()
    msg['Subject'] = 'Confirmación correo'
    msg['From'] = _my_email
    msg['To'] = email
    msg.set_content(
        render,
        subtype='html',
    )

    # with smtplib.SMTP_SSL('smtp.gmail.com', port=465) as smtp:
    #     smtp.login(_my_email, _my_pwd)
    #     smtp.send_message(msg)

    with smtplib.SMTP(
        settings.smtp_domain_email,
        port=settings.smtp_port_email,
    ) as smtp:
        smtp.send_message(
            msg=msg,
            from_addr=_my_email,
            to_addrs=email,
        )
