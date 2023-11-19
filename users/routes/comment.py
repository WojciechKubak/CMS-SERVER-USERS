from users.service.configuration import comment_service
from users.forms.comment import CommentForm
from flask import Response, make_response
from flask_restful import Resource, reqparse


class CommentIdResource(Resource):

    def get(self, id_: str) -> Response:
        try:
            user = comment_service.get_comment_by_id(id_)
            return make_response(user.to_json(), 200)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)

    def delete(self, id_: str) -> Response:
        try:
            id_ = comment_service.delete_comment(id_)
            return make_response({'message': f'Deleted user with id: {id_}'}, 200)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)


class AddCommentResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('content', type=str)
    parser.add_argument('article_id', type=int)
    parser.add_argument('user_id', type=int)

    def post(self) -> Response:
        data = AddCommentResource.parser.parse_args()
        form = CommentForm(data=data)
        if form.validate():
            try:
                comment = comment_service.add_comment(data)
                return make_response(comment.to_json(), 201)
            except ValueError as e:
                return make_response({'message': e.args[0]}, 400)
        return make_response(form.errors, 400)


class CommentContentResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('content', type=str)
    parser.add_argument('article_id', type=int)
    parser.add_argument('user_id', type=int)

    def put(self, id_: int) -> Response:
        data = CommentContentResource.parser.parse_args()
        form = CommentForm(data=data)
        if form.validate():
            try:
                comment = comment_service.update_comment_content(data | {'id': id_})
                return make_response(comment.to_json(), 200)
            except ValueError as e:
                return make_response({'message': e.args[0]}, 400)
        return make_response(form.errors, 400)


class CommentUserIdResource(Resource):

    def get(self, id_: int) -> Response:
        comments = comment_service.get_user_comments(id_)
        return make_response([comment.to_json() for comment in comments], 200)


class CommentArticleIdResource(Resource):

    def get(self, id_: int) -> Response:
        comments = comment_service.get_article_comments(id_)
        return make_response([comment.to_json() for comment in comments], 200)
