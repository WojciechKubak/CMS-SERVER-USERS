from users.routes.user import UserResource, UserRegisterResource
from users.web.configuration import app
from users.db.configuration import sa
from users.config import get_config
from flask import Flask, Response, make_response
from flask_restful import Api
from werkzeug.middleware.proxy_fix import ProxyFix
import logging


def create_app() -> Flask:

    logging.basicConfig(level=logging.INFO)
    env_config = get_config()

    with app.app_context():

        app.config.from_object(env_config)

        sa.init_app(app)

        app.wsgi_app = ProxyFix(
            app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=0
        )

        api = Api(app)

        api.add_resource(UserResource, '/users/<string:username>')
        api.add_resource(UserRegisterResource, '/register')

        @app.route('/')
        def index() -> Response:
            return make_response({'message': 'Users home page'}, 200)

        return app
