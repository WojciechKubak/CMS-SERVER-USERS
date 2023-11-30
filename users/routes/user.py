from users.security.token_required import jwt_required_with_roles
from users.service.configuration import user_service
from users.forms.user import RegistrationForm
from flask import Response, make_response, request
from flask_restful import Resource, reqparse
from datetime import datetime


class UserIdResource(Resource):
    """Flask-RESTful resource for handling individual users by ID."""
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('email', type=str, required=True)
    parser.add_argument('password', type=str, required=True)
    parser.add_argument('role', type=str)
    parser.add_argument('is_active', type=bool)

    @jwt_required_with_roles(['admin'])
    def get(self, id_: str) -> Response:
        """
        Get a user by ID.

        Args:
            id_ (str): The ID of the user.

        Returns:
            Response: The HTTP response containing the user data or an error message.
        """
        try:
            user = user_service.get_user_by_id(id_)
            return make_response(user.to_json(), 200)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)

    @jwt_required_with_roles(['admin'])
    def put(self, id_: str) -> Response:
        """
        Update a user by ID.

        Args:
            id_ (str): The ID of the user.

        Returns:
            Response: The HTTP response containing the updated user data or an error message.
        """
        data = UserIdResource.parser.parse_args()
        try:
            user = user_service.update_user(data | {'id': id_})
            return make_response(user.to_json(), 200)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)

    @jwt_required_with_roles(['admin'])
    def delete(self, id_: str) -> Response:
        """
        Delete a user by ID.

        Args:
            id_ (str): The ID of the user.

        Returns:
            Response: The HTTP response confirming the deletion or an error message.
        """
        try:
            id_ = user_service.delete_user(id_)
            return make_response({'message': f'Deleted user with id: {id_}'}, 200)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)


class UserNameResource(Resource):
    """Flask-RESTful resource for handling users by username."""
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str)
    parser.add_argument('password', type=str)

    @jwt_required_with_roles(['user', 'redactor', 'translator', 'admin'])
    def get(self, username: str) -> Response:
        """
        Get a user by username.

        Args:
            username (str): The username of the user.

        Returns:
            Response: The HTTP response containing the user data or an error message.
        """
        try:
            user = user_service.get_user_by_name(username)
            return make_response(user.to_json(), 200)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)


class UserListResource(Resource):
    """A Flask-RESTful resource for handling lists of users."""

    @jwt_required_with_roles(['admin'])
    def get(self) -> Response:
        """
        Get a list of all users.

        Returns:
            Response: The HTTP response containing the list of users or an error message.
        """
        users = user_service.get_all_users()
        return make_response({'users': [user.to_json() for user in users]}, 200)


class UserRegisterResource(Resource):
    """Flask-RESTful resource for handling user registration."""
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str)
    parser.add_argument('email', type=str)
    parser.add_argument('password', type=str)

    def post(self) -> Response:
        """
        Register a new user.

        Returns:
            Response: The HTTP response containing the registered user data or an error message.
        """
        data = UserRegisterResource.parser.parse_args()
        form = RegistrationForm(data=data)
        if form.validate():
            try:
                user = user_service.register_user(data)
                return make_response(user.to_json(), 201)
            except ValueError as e:
                return make_response({'message': e.args[0]}, 400)
        return make_response(form.errors, 400)


class UserActivationResource(Resource):
    """Flask-RESTful resource for handling user activation."""

    def get(self) -> Response:
        """
        Activate a user based on activation link parameters.

        Returns:
            Response: The HTTP response confirming the activation or an error message.
        """
        timestamp = float(request.args.get('timestamp'))
        if timestamp < datetime.utcnow().timestamp() * 1000:
            return make_response({'message': 'Activation link expired'}, 400)
        try:
            user_service.activate_user(request.args.get('id'))
            return make_response({'message': 'User activated'}, 200)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)
