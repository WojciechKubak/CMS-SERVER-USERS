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
from users.routes.comment import (
    CommentIdResource,
    CommentResource,
    CommentContentResource,
    CommentUserIdResource,
    CommentArticleIdResource
)
from flask import Flask, Response, make_response
from flask_restful import Api
from jinja2 import PackageLoader, Environment
from werkzeug.middleware.proxy_fix import ProxyFix
import logging


def create_app() -> Flask:
    """
    Factory function for creating the Flask application.

    Returns:
        Flask: The configured Flask application.
    """

    # Set up logging
    logging.basicConfig(level=logging.INFO)

    with app.app_context():

        # Configure ProxyFix for handling reverse proxy headers
        app.wsgi_app = ProxyFix(
            app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=0
        )

        # Configure application with settings from app_config
        app.config.from_object(app_config)

        # Initialize SQLAlchemy with the Flask application
        sa.init_app(app)

        # Configure security settings
        app.config.update(security_config)
        jwt_manager.init_app(app)
        configure_security(app)
        bcrypt.init_app(app)

        # Configure email settings
        app.config.update(mail_config)
        templates_env = Environment(loader=PackageLoader('users.email', 'templates'))
        MailConfig.prepare_mail(app, templates_env)

        @app.route('/')
        def index() -> Response:
            """Default route handler for the home page."""
            return make_response({'message': 'Users home page'}, 200)

        # Create API endpoints for user and comment resources
        api = Api(app)
        api.add_resource(UserIdResource, '/users/<int:id_>')
        api.add_resource(UserNameResource, '/users/<string:username>')
        api.add_resource(UserListResource, '/users')
        api.add_resource(UserActivationResource, '/users/activate')
        api.add_resource(UserRegisterResource, '/users/register')

        api.add_resource(CommentIdResource, '/comments/<int:id_>')
        api.add_resource(CommentResource, '/comments/')
        api.add_resource(CommentContentResource, '/comments/<int:id_>')
        api.add_resource(CommentUserIdResource, '/comments/user/<int:id_>')
        api.add_resource(CommentArticleIdResource, '/comments/article/<int:id_>')

        return app
