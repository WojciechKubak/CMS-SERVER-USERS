from users.web.configuration import app
from flask import make_response, Response


@app.errorhandler(404)
def not_found_error(error: int) -> Response:
    return make_response({'message': 'The requested resource was not found.'}, error)


@app.errorhandler(500)
def internal_server_error(error: int) -> Response:
    return make_response({'message': 'Internal server error'}, error)


@app.errorhandler(400)
def bad_request_error(error: int) -> Response:
    return make_response({'message': 'Bad request'}, error)
