from users.config import mail_config
from users.email.configuration import MailConfig
from users.db.configuration import sa
from users.model.user import UserModel
from users.security.configure_security import configure_security
from users.config import security_config
from jinja2 import PackageLoader, Environment
from flask.testing import Client
from flask_jwt_extended import JWTManager
from flask import Flask
from typing import Any
import pytest


@pytest.fixture(autouse=True)
def app(app: Flask) -> Flask:
    app.config.update(security_config)

    jwt_manager = JWTManager(app)
    jwt_manager.init_app(app)
    configure_security(app)

    templates_env = Environment(
        loader=PackageLoader('users.email', 'templates'))

    app.config.update(mail_config)
    MailConfig.prepare_mail(app, templates_env)

    yield app


@pytest.fixture(autouse=True)
def client(client: Client, access_token: str, app: Flask) -> Client:
    client.set_cookie('access_token_cookie', access_token)
    yield client


@pytest.fixture(autouse=True)
def add_user(app: Flask, user_model_data: dict[str, Any]) -> None:
    sa.session.add(UserModel(**user_model_data))
    sa.session.commit()
