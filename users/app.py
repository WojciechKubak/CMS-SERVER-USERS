from flask import Flask, Response, make_response

app = Flask(__name__)


def create_app() -> Flask:

    with app.app_context():

        @app.route('/')
        def index() -> Response:
            return make_response({'message': 'Users home page'}, 200)

        return app
