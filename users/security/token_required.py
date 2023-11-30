from users.service.configuration import user_service
from users.web.configuration import app
from flask_jwt_extended import verify_jwt_in_request, create_access_token, set_access_cookies, get_jwt_identity, get_jwt
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError
from flask import Response, make_response
from datetime import datetime, timezone, timedelta
from typing import Callable, Any
from functools import wraps
import os


def jwt_required_with_roles(roles: list[str]) -> Callable:
    """
    Decorator function to require JWT with specified roles for accessing a route.

    Args:
        roles (list[str]): List of roles required for accessing the route.

    Returns:
        Callable: Decorator function.
    """
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def decorated(*args: tuple[Any], **kwargs: dict[str, Any]) -> Response:
            """
            Decorated function to check JWT and roles before executing the original function.

            Args:
                *args (tuple[Any]): Additional arguments passed to the function.
                **kwargs (dict[str, Any]): Additional keyword arguments passed to the function.

            Returns:
                Response: The result of the original function or an HTTP response if the conditions are not met.
            """
            try:
                verify_jwt_in_request()
                user_id = get_jwt().get('sub')
                user_role = user_service.get_user_by_id(user_id).role.lower()
                if user_role in roles:
                    return fn(*args, **kwargs)
                else:
                    return make_response({'message': 'Insufficient permissions'}, 403)
            except (NoAuthorizationError, InvalidHeaderError):
                return make_response({'message': 'Token is missing or invalid'}, 401)

        return decorated
    return decorator


@app.after_request
def refresh_expiring_jwts(response: Response) -> Response:
    """
    After-request handler to refresh expiring JWTs.

    Args:
        response (Response): The HTTP response.

    Returns:
        Response: The modified HTTP response.
    """
    try:
        refresh_token_data = get_jwt()
        refresh_exp, role = refresh_token_data['exp'], refresh_token_data['role']

        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(seconds=int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES'))))
        if target_timestamp > refresh_exp:
            access_token = create_access_token(identity=get_jwt_identity(), additional_claims={'role': role})
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response
