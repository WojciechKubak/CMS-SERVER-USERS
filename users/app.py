from users.routes.user import UserIdResource, UserNameResource, UserListResource
from users.routes.email import UserActivationResource, UserRegisterResource
from users.security.configure_security import configure_security
from users.email.configuration import MailConfig
from users.web.configuration import app
from users.config import get_configuration
from flask import Flask, Response, make_response
from flask_jwt_extended import JWTManager
from flask_restful import Api
from jinja2 import PackageLoader, Environment
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv
import tomllib
import logging
import os


def create_app() -> Flask:

    logging.basicConfig(level=logging.INFO)
    load_dotenv()

    with app.app_context():

        app.wsgi_app = ProxyFix(
            app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=0
        )

        config = get_configuration()
        app.config.from_object(config)
        base_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        config_file_path = os.path.join(base_dir, 'users', 'config.toml')
        app.config.from_file(config_file_path, load=tomllib.load, text=False)

        manager = JWTManager(app)
        configure_security(app)

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
