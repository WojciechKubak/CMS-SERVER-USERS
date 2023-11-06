from users.security.token_required import jwt_required_with_roles
from users.service.configuration import user_service
from flask import Response, make_response
from flask_restful import Resource, reqparse


class UserIdResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str)
    parser.add_argument('email', type=str)
    parser.add_argument('password', type=str)
    parser.add_argument('role', type=str)
    parser.add_argument('is_active', type=bool)

    @jwt_required_with_roles(['admin'])
    def get(self, id_: str) -> Response:
        try:
            user = user_service.get_user_by_id(id_)
            return make_response(user.to_json(), 200)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)

    @jwt_required_with_roles(['admin'])
    def put(self, id_: str) -> Response:
        data = UserIdResource.parser.parse_args()
        try:
            user = user_service.update_user(data | {'id': id_})
            return make_response(user.to_json(), 201)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)

    @jwt_required_with_roles(['admin'])
    def delete(self, id_: str) -> Response:
        try:
            id_ = user_service.delete_user(id_)
            return make_response({'message': f'Deleted user with id: {id_}'}, 200)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)


class UserNameResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str)
    parser.add_argument('password', type=str)
    parser.add_argument('role', type=str)
    parser.add_argument('is_active', type=bool)

    @jwt_required_with_roles(['user', 'redactor', 'translator', 'admin'])
    def get(self, username: str) -> Response:
        try:
            user = user_service.get_user_by_name(username)
            return make_response(user.to_json(), 200)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)

    @jwt_required_with_roles(['admin'])
    def post(self, username: str) -> Response:
        data = UserNameResource.parser.parse_args()
        try:
            user = user_service.add_user(data | {'username': username})
            return make_response(user.to_json(), 201)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)


class UserListResource(Resource):

    @jwt_required_with_roles(['admin'])
    def get(self) -> Response:
        users = user_service.get_all_users()
        return make_response({'users': [user.to_json() for user in users]}, 200)
