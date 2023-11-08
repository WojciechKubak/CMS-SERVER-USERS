from users.service.configuration import user_service
from users.forms.registration import RegistrationForm
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
        form = RegistrationForm(data=data)
        if form.validate():
            try:
                user = user_service.register_user(data)
                return make_response(user.to_json(), 201)
            except ValueError as e:
                return make_response({'message': e.args[0]}, 400)
        return make_response(form.errors, 400)


class UserActivationResource(Resource):

    def get(self) -> Response:
        timestamp = float(request.args.get('timestamp'))
        if timestamp < datetime.utcnow().timestamp() * 1000:
            return make_response({'message': 'Activation link expired'}, 400)
        try:
            user_service.activate_user(request.args.get('id'))
            return make_response({'message': 'User activated'}, 200)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)
