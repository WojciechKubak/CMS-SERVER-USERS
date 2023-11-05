from users.security.token_required import jwt_required_with_roles
from users.service.configuration import user_service
from flask import make_response, request, Response
from flask_restful import Resource, reqparse
from datetime import datetime


class UserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str)
    parser.add_argument('password', type=str)
    parser.add_argument('role', type=str)

    @jwt_required_with_roles(['user', 'redactor', 'translator', 'admin'])
    def get(self, username: str) -> Response:
        try:
            user = user_service.get_user_by_name(username)
            return make_response(user.to_json(), 200)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)

    @jwt_required_with_roles(['admin'])
    def post(self, username: str) -> Response:
        data = UserResource.parser.parse_args()
        try:
            user = user_service.add_user(data | {'username': username})
            return make_response(user.to_json(), 201)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)

    @jwt_required_with_roles(['admin'])
    def put(self, username: str) -> Response:
        data = UserResource.parser.parse_args()
        try:
            user = user_service.update_user(data | {'username': username})
            return make_response(user.to_json(), 201)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)

    @jwt_required_with_roles(['admin'])
    def delete(self, username: str) -> Response:
        try:
            id_ = user_service.delete_user(username)
            return make_response({'message': f'Deleted user with id: {id_}'}, 200)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)


class UserListResource(Resource):

    @jwt_required_with_roles(['admin'])
    def get(self) -> Response:
        users = user_service.get_all_users()
        return make_response({'users': [user.to_json() for user in users]}, 200)


class UserRegisterResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str)
    parser.add_argument('email', type=str)
    parser.add_argument('password', type=str)

    def post(self) -> Response:
        data = UserRegisterResource.parser.parse_args()
        try:
            user = user_service.register_user(data)
            return make_response(user.to_json(), 201)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)


class UserActivationResource(Resource):

    def get(self) -> Response:
        timestamp = float(request.args.get('timestamp'))
        if timestamp < datetime.utcnow().timestamp() * 1000:
            return make_response({'message': 'Activation link expired'}, 400)
        try:
            user = user_service.get_user_by_name(request.args.get('username'))
            user_service.activate_user(user.username)
            return make_response({'message': 'User activated'}, 200)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)
