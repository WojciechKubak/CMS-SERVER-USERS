from users.routes.user import UserIdResource, UserNameResource, UserListResource
from users.routes.email import UserActivationResource, UserRegisterResource
from users.security.configure_security import configure_security
from users.email.configuration import MailConfig
from users.web.configuration import app
from users.config import call_configuration

from flask import Flask, Response, make_response
from flask_jwt_extended import JWTManager
from flask_restful import Api

from jinja2 import PackageLoader, Environment
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv
import logging
import ast
import os


def create_app() -> Flask:

    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    config = call_configuration()

    with app.app_context():

        app.wsgi_app = ProxyFix(
            app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=0
        )

        app.config.from_object(config)

        setup_security_envs(app)
        manager = JWTManager(app)
        configure_security(app)

        setup_email_envs(app)
        templates_env = Environment(loader=PackageLoader('users', 'templates'))
        MailConfig.prepare_mail(app, templates_env)

        setup_routing(app)

        return app


def setup_security_envs(flask_app: Flask) -> None:
    jwt_settings = {
        'JWT_COOKIE_SECURE': ast.literal_eval(os.environ.get('JWT_COOKIE_SECURE')),
        'JWT_TOKEN_LOCATION': ast.literal_eval(os.environ.get('JWT_TOKEN_LOCATION')),
        'JWT_SECRET_KEY': os.environ.get('JWT_SECRET_KEY'),
        'JWT_ACCESS_TOKEN_EXPIRES': int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES')),
        'JWT_REFRESH_TOKEN_EXPIRES': int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES')),
        'JWT_COOKIE_CSRF_PROTECT': ast.literal_eval(os.environ.get('JWT_COOKIE_CSRF_PROTECT'))
    }
    flask_app.config.update(jwt_settings)


def setup_email_envs(flask_app: Flask) -> None:
    mail_settings = {
        'MAIL_SERVER': os.environ.get('MAIL_SERVER'),
        'MAIL_PORT': int(os.environ.get('MAIL_PORT')),
        'MAIL_USE_SSL': ast.literal_eval(os.environ.get('MAIL_USE_SSL')),
        'MAIL_USE_TLS': ast.literal_eval(os.environ.get('MAIL_USE_TLS')),
        'MAIL_USERNAME': os.environ.get('MAIL_USERNAME'),
        'MAIL_PASSWORD': os.environ.get('MAIL_PASSWORD')
    }
    flask_app.config.update(mail_settings)


def setup_routing(flask_app: Flask) -> None:
    @app.route('/')
    def index() -> Response:
        return make_response({'message': 'Users home page'}, 200)

    api = Api(flask_app)
    api.add_resource(UserIdResource, '/users/<int:id_>')
    api.add_resource(UserNameResource, '/users/<string:username>')
    api.add_resource(UserListResource, '/users')
    api.add_resource(UserActivationResource, '/users/activate')
    api.add_resource(UserRegisterResource, '/users/register')
