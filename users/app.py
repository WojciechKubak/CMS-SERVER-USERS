from users.routes.user import UserResource, UserListResource, UserRegisterResource
from users.security.configure_security import configure_security
from users.web.configuration import app
from users.db.configuration import sa
from users.config import get_config

from flask import Flask, Response, make_response
from flask_jwt_extended import JWTManager
from flask_restful import Api

from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv
import logging
import ast
import os


def create_app() -> Flask:

    logging.basicConfig(level=logging.INFO)
    load_dotenv()

    with app.app_context():

        app.wsgi_app = ProxyFix(
            app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=0
        )

        env_config = get_config()
        app.config.from_object(env_config)
        sa.init_app(app)

        jwt_settings = {
            'JWT_COOKIE_SECURE': ast.literal_eval(os.environ.get('JWT_COOKIE_SECURE')),
            'JWT_TOKEN_LOCATION': ast.literal_eval(os.environ.get('JWT_TOKEN_LOCATION')),
            'JWT_SECRET_KEY': os.environ.get('JWT_SECRET_KEY'),
            'JWT_ACCESS_TOKEN_EXPIRES': int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES')),
            'JWT_REFRESH_TOKEN_EXPIRES': int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES')),
            'JWT_COOKIE_CSRF_PROTECT': ast.literal_eval(os.environ.get('JWT_COOKIE_CSRF_PROTECT'))
        }
        app.config.update(jwt_settings)
        manager = JWTManager(app)
        configure_security(app)

        api = Api(app)
        api.add_resource(UserListResource, '/users')
        api.add_resource(UserResource, '/users/<string:username>')
        api.add_resource(UserRegisterResource, '/register')

        @app.route('/')
        def index() -> Response:
            return make_response({'message': 'Users home page'}, 200)

        return app
