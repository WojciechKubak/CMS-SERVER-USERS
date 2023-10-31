from users.web.configuration import app
from flask import Flask, Response, make_response
from werkzeug.middleware.proxy_fix import ProxyFix


def create_app() -> Flask:

    with app.app_context():

        app.wsgi_app = ProxyFix(
            app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=0
        )

        @app.route('/')
        def index() -> Response:
            return make_response({'message': 'Users home page'}, 200)

        return app
