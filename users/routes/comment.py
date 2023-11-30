from users.service.configuration import comment_service
from users.forms.comment import CommentForm
from flask import Response, make_response
from flask_restful import Resource, reqparse


class CommentIdResource(Resource):
    """
    CommentIdResource Class

    A Flask-RESTful resource for handling individual comments by ID.
    """

    def get(self, id_: str) -> Response:
        """
        Get a comment by ID.

        Args:
            id_ (str): The ID of the comment.

        Returns:
            Response: The HTTP response containing the comment data or an error message.
        """
        try:
            user = comment_service.get_comment_by_id(id_)
            return make_response(user.to_json(), 200)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)

    def delete(self, id_: str) -> Response:
        """
        Delete a comment by ID.

        Args:
            id_ (str): The ID of the comment.

        Returns:
            Response: The HTTP response confirming the deletion or an error message.
        """
        try:
            id_ = comment_service.delete_comment(id_)
            return make_response({'message': f'Deleted user with id: {id_}'}, 200)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)


class CommentResource(Resource):
    """
    CommentResource Class

    A Flask-RESTful resource for handling comments.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('content', type=str)
    parser.add_argument('article_id', type=int)
    parser.add_argument('user_id', type=int)

    def post(self) -> Response:
        """
        Add a new comment.

        Returns:
            Response: The HTTP response containing the added comment data or an error message.
        """
        data = CommentResource.parser.parse_args()
        form = CommentForm(data=data)
        if form.validate():
            try:
                comment = comment_service.add_comment(data)
                return make_response(comment.to_json(), 201)
            except ValueError as e:
                return make_response({'message': e.args[0]}, 400)
        return make_response(form.errors, 400)


class CommentContentResource(Resource):
    """
    CommentContentResource Class

    A Flask-RESTful resource for handling comment content updates.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('content', type=str)
    parser.add_argument('article_id', type=int)
    parser.add_argument('user_id', type=int)

    def put(self, id_: int) -> Response:
        """
        Update comment content by ID.

        Args:
            id_ (int): The ID of the comment.

        Returns:
            Response: The HTTP response containing the updated comment data or an error message.
        """
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
    """
    CommentUserIdResource Class

    A Flask-RESTful resource for handling comments by user ID.
    """

    def get(self, id_: int) -> Response:
        """
        Get comments by user ID.

        Args:
            id_ (int): The ID of the user.

        Returns:
            Response: The HTTP response containing the user's comments or an error message.
        """
        try:
            comments = comment_service.get_user_comments(id_)
            return make_response([comment.to_json() for comment in comments], 200)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)


class CommentArticleIdResource(Resource):
    """
    CommentArticleIdResource Class

    A Flask-RESTful resource for handling comments by article ID.
    """

    def get(self, id_: int) -> Response:
        """
        Get comments by article ID.

        Args:
            id_ (int): The ID of the article.

        Returns:
            Response: The HTTP response containing the article's comments or an error message.
        """
        try:
            comments = comment_service.get_article_comments(id_)
            return make_response([comment.to_json() for comment in comments], 200)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)
