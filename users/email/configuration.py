from flask_mail import Mail, Message
from flask import Flask
from dataclasses import dataclass, field
from jinja2 import Environment
from datetime import datetime
from typing import Self
import os


@dataclass
class MailConfig:
    """
    MailConfig Class

    This class provides methods for configuring and sending emails.

    Attributes:
        mail (Mail): An instance of the Flask-Mail class for managing email functionality.
        template_env (Environment): An instance of the Jinja2 Environment class for rendering email templates.
    """
    mail: Mail = field(default=None, init=False)
    template_env: Environment = field(default=None, init=False)

    @classmethod
    def prepare_mail(cls: Self, app: Flask, template_env: Environment) -> None:
        """
        Prepare Mail Configuration

        Configures the MailConfig class with a Flask app and a Jinja2 template environment.

        Args:
            app (Flask): The Flask app instance.
            template_env (Environment): The Jinja2 template environment.

        Returns:
            None
        """
        cls.mail = Mail(app)
        cls.template_env = template_env

    @classmethod
    def send_activation_mail(cls: Self, id_: int, email: str) -> None:
        """
        Send Activation Mail

        Sends an activation email to the specified email address with an activation link.

        Args:
            id_ (int): The user ID for activation.
            email (str): The email address to which the activation email is sent.

        Returns:
            None
        """
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
