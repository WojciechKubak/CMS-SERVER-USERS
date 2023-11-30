from users.routes.user import (
    UserIdResource,
    UserNameResource,
    UserListResource,
    UserRegisterResource,
    UserActivationResource
)
from flask_restful import Api
from flask import Flask
import pytest


@pytest.fixture(autouse=True)
def app(app: Flask) -> Flask:
    api = Api(app)

    api.add_resource(UserIdResource, '/users/<int:id_>')
    api.add_resource(UserNameResource, '/users/<string:username>')
    api.add_resource(UserListResource, '/users')
    api.add_resource(UserActivationResource, '/users/activate')
    api.add_resource(UserRegisterResource, '/users/register')

    yield app
