from flask_mail import Mail, Message
from flask import Flask
from dataclasses import dataclass, field
from jinja2 import Environment
from datetime import datetime
from typing import Self
import os


@dataclass
class MailConfig:
    mail: Mail = field(default=None, init=False)
    template_env: Environment = field(default=None, init=False)

    @classmethod
    def prepare_mail(cls: Self, app: Flask, template_env: Environment) -> None:
        cls.mail = Mail(app)
        cls.template_env = template_env

    @classmethod
    def send_activation_mail(cls: Self, id_: int, email: str) -> None:
        timestamp = datetime.utcnow().timestamp() * 1000 + int(os.getenv('REGISTER_TOKEN_LIFESPAN'))
        activation_url = f'http://localhost/users/activate?id={id_}&timestamp={timestamp}'
        template = cls.template_env.get_template('activation_mail.html')
        html_body = template.render(activation_url=activation_url)

        message = Message(
            subject='Activate your account',
            sender=os.environ.get('MAIL_USERNAME'),
            recipients=[email],
            html=html_body
        )
        MailConfig.mail.send(message)
