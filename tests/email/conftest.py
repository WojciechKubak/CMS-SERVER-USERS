from users.config import mail_config
from users.email.configuration import MailConfig
from jinja2 import PackageLoader, Environment
from flask import Flask
import pytest


@pytest.fixture(scope='function')
def app(app: Flask):

    templates_env = Environment(
        loader=PackageLoader('users.email', 'templates'))

    app.config.update(mail_config)
    MailConfig.prepare_mail(app, templates_env)

    yield app
