from users.model.user import UserModel
from users.model.comment import CommentModel
from dataclasses import dataclass
from typing import Any


@dataclass
class CommentService:

    def add_comment(self, data: dict[str, Any]) -> CommentModel:
        if not UserModel.find_by_id(data.get('user_id')):
            raise ValueError('User not found.')
        comment = CommentModel.from_json(data)
        comment.add()
        return comment

    def update_comment_content(self, data: dict[str, Any]) -> CommentModel:
        result = CommentModel.find_by_id(data.get('id'))
        if not result:
            raise ValueError('Comment not found')
        comment = CommentModel.from_json(data)
        if result != comment:
            raise ValueError('Comment are not the same')
        comment.update()
        return comment

    def delete_comment(self, id_: int) -> int:
        result = CommentModel.find_by_id(id_)
        if not result:
            raise ValueError('Comment not found')
        result.delete()
        return result.id

    def get_comment_by_id(self, id_: int) -> CommentModel:
        result = CommentModel.find_by_id(id_)
        if not result:
            raise ValueError('Comment not found')
        return result

    def get_user_comments(self, user_id: int) -> list[CommentModel]:
        return CommentModel.query.filter_by(user_id=user_id).all()

    def get_article_comments(self, article_id: int) -> list[CommentModel]:
        return CommentModel.query.filter_by(article_id=article_id).all()
