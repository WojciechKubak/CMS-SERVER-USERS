from users.config import app_config
from users.security.configuration import bcrypt
from users.db.configuration import sa
from flask_jwt_extended import create_access_token
from flask.testing import Client
from flask import Flask
from typing import Any, Callable
import pytest


@pytest.fixture
def app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(app_config)
    yield app


@pytest.fixture(autouse=True)
def db_setup_and_teardown(app: Flask):
    sa.init_app(app)

    with app.app_context():
        sa.create_all()

        yield app

    with app.app_context():
        sa.drop_all()


@pytest.fixture
def client(app: Flask) -> Client:
    with app.test_client() as client:
        yield client


@pytest.fixture
def access_token(user_model_data: dict[str, Any]) -> Callable[[Any], str]:
    return create_access_token(identity=user_model_data['id'])


@pytest.fixture(scope='session')
def user_dto() -> dict[str, Any]:
    return {
        'username': 'User',
        'email': 'user@example.com',
        'password': '123456'
    }


@pytest.fixture(scope='session')
def comment_dto(user_model_data: dict[str, Any]) -> dict[str, Any]:
    return {
        'content': 'dummy content',
        'article_id': 1,
        'user_id': user_model_data['id']
    }


@pytest.fixture(scope='session')
def user_model_data(user_dto: dict[str, Any]) -> dict[str, Any]:
    return user_dto | {
        'id': 1,
        'role': 'admin',
        'is_active': False,
        'password': bcrypt.generate_password_hash(user_dto['password']).decode('utf8')
    }


@pytest.fixture(scope='session')
def comment_model_data(comment_dto: dict[str, Any]) -> dict[str, Any]:
    return comment_dto | {'id': 1}
