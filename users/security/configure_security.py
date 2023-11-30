from users.service.configuration import user_service
from users.forms.user import LoginForm
from flask import Flask, Response, request, make_response
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies
)


def configure_security(app: Flask) -> None:
    """
    Configure security-related endpoints and JWT authentication for the Flask app.

    Args:
        app (Flask): The Flask app to configure.

    Returns:
        None
    """

    @app.post('/login')
    def login() -> Response:
        """
        Handle user login and issue JWT tokens.

        Returns:
            Response: A response indicating whether the login was successful or an error message.
        """
        data = request.get_json()

        form = LoginForm(data=data)
        if not form.validate():
            return make_response(form.errors, 400)

        try:
            username, password = data.get('username'), data.get('password')

            if not username or not password:
                return make_response({'message': 'No credentials provided'}, 400)

            user = user_service.check_login_credentials(username, password)

            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)

            response = make_response({'message': "Login successful"})
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            return response

        except ValueError as e:
            return make_response({'message': e.args[0]}, 401)

    @app.post('/logout')
    def logout() -> Response:
        """
        Handle user logout by unsetting JWT cookies.

        Returns:
            Response: A response indicating whether the logout was successful.
        """
        response = make_response({'message': "Logout successful"})
        unset_jwt_cookies(response)
        return response
