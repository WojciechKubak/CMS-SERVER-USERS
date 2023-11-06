from users.service.configuration import user_service
from flask import make_response, request, Response
from flask_restful import Resource, reqparse
from datetime import datetime


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
