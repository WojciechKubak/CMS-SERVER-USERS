from users.config import app_config, security_config, mail_config
from users.security.configure_security import configure_security
from users.security.configuration import jwt_manager, bcrypt
from users.db.configuration import sa
from users.email.configuration import MailConfig
from users.web.configuration import app
from users.routes.user import (
    UserIdResource,
    UserNameResource,
    UserListResource,
    UserRegisterResource,
    UserActivationResource
)
from flask import Flask, Response, make_response
from flask_restful import Api
from jinja2 import PackageLoader, Environment
from werkzeug.middleware.proxy_fix import ProxyFix
import logging


def create_app() -> Flask:

    logging.basicConfig(level=logging.INFO)

    with app.app_context():

        app.wsgi_app = ProxyFix(
            app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=0
        )

        app.config.from_object(app_config)

        sa.init_app(app)

        app.config.update(security_config)
        jwt_manager.init_app(app)
        configure_security(app)
        bcrypt.init_app(app)

        app.config.update(mail_config)
        templates_env = Environment(loader=PackageLoader('users.email', 'templates'))
        MailConfig.prepare_mail(app, templates_env)

        @app.route('/')
        def index() -> Response:
            return make_response({'message': 'Users home page'}, 200)

        api = Api(app)
        api.add_resource(UserIdResource, '/users/<int:id_>')
        api.add_resource(UserNameResource, '/users/<string:username>')
        api.add_resource(UserListResource, '/users')
        api.add_resource(UserActivationResource, '/users/activate')
        api.add_resource(UserRegisterResource, '/users/register')

        return app
