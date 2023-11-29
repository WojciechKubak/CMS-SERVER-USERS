from users.routes.comment import (
    CommentIdResource,
    AddCommentResource,
    CommentContentResource,
    CommentUserIdResource,
    CommentArticleIdResource
)
from users.model.comment import CommentModel
from users.db.configuration import sa
from flask_restful import Api
from flask import Flask
from typing import Any
import pytest


@pytest.fixture(scope='function', autouse=True)
def add_comment(app: Flask, comment_model_data: dict[str, Any]) -> None:
    sa.session.add(CommentModel(**comment_model_data))
    sa.session.commit()


@pytest.fixture(autouse=True)
def add_routing(app: Flask) -> Flask:
    api = Api(app)

    api.add_resource(CommentIdResource, '/comments/<int:id_>')
    api.add_resource(AddCommentResource, '/comments/')
    api.add_resource(CommentContentResource, '/comments/<int:id_>')
    api.add_resource(CommentUserIdResource, '/comments/user/<int:id_>')
    api.add_resource(CommentArticleIdResource, '/comments/article/<int:id_>')

    yield app
