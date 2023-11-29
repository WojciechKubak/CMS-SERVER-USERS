from users.security.configure_security import configure_security
from users.security.token_required import jwt_required_with_roles
from users.config import security_config
from users.model.user import UserModel
from users.db.configuration import sa
from flask import Flask, Response, make_response
from flask_jwt_extended import JWTManager
from typing import Any
import pytest


@pytest.fixture(scope='function')
def app(app: Flask) -> Flask:

    app.config.update(security_config)
    JWTManager(app)
    configure_security(app)

    @app.get('/resource')
    @jwt_required_with_roles(['admin'])
    def foo() -> Response:
        return make_response({'message': 'content'}, 200)

    yield app


@pytest.fixture(scope='function', autouse=True)
def add_user(app: Flask, user_model_data: dict[str, Any]) -> None:
    sa.session.add(UserModel(**user_model_data))
    sa.session.commit()
