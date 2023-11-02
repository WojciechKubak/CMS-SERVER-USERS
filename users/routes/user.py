from users.service.user import UserService
from users.security.token_required import jwt_required_with_roles
from flask_restful import Resource, reqparse
from flask import make_response, Response


class UserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str)
    parser.add_argument('password', type=str)
    parser.add_argument('role', type=str)

    @jwt_required_with_roles(['user', 'redactor', 'translator', 'admin'])
    def get(self, username: str) -> Response:
        try:
            user = UserService().get_user_by_name(username)
            return make_response(user.to_json(), 200)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)

    @jwt_required_with_roles(['admin'])
    def post(self, username: str) -> Response:
        data = UserResource.parser.parse_args()
        try:
            user = UserService().add_user(data | {'username': username})
            return make_response(user.to_json(), 201)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)

    @jwt_required_with_roles(['admin'])
    def put(self, username: str) -> Response:
        data = UserResource.parser.parse_args()
        try:
            user = UserService().update_user(data | {'username': username})
            return make_response(user.to_json(), 201)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)

    @jwt_required_with_roles(['admin'])
    def delete(self, username: str) -> Response:
        try:
            id_ = UserService().delete_user(username)
            return make_response({'message': f'Deleted user with id: {id_}'})
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)


class UserListResource(Resource):

    @jwt_required_with_roles(['admin'])
    def get(self) -> Response:
        users = UserService().get_all_users()
        return make_response({'users': [user.to_json() for user in users]}, 200)


class UserRegisterResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str)
    parser.add_argument('email', type=str)
    parser.add_argument('password', type=str)

    def post(self) -> Response:
        data = UserRegisterResource.parser.parse_args()
        try:
            user = UserService().register_user(data)
            return make_response(user.to_json(), 201)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)