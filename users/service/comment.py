from users.model.user import UserModel
from users.model.comment import CommentModel
from dataclasses import dataclass
from typing import Any


@dataclass
class CommentService:
    """Service class for handling operations related to comments."""

    def add_comment(self, data: dict[str, Any]) -> CommentModel:
        """
        Add a new comment based on the provided data.

        Args:
            data (dict[str, Any]): Data for creating the new comment.

        Returns:
            CommentModel: The created comment.
        """
        if not UserModel.find_by_id(data.get('user_id')):
            raise ValueError('User not found')
        comment = CommentModel.from_json(data)
        comment.add()
        return comment

    def update_comment_content(self, data: dict[str, Any]) -> CommentModel:
        """
        Update the content of a comment based on the provided data.

        Args:
            data (dict[str, Any]): Data for updating the comment content.

        Returns:
            CommentModel: The updated comment.
        """
        result = CommentModel.find_by_id(data.get('id'))
        if not result:
            raise ValueError('Comment not found')
        comment = CommentModel.from_json(data)
        if result != comment:
            raise ValueError('Comment are not the same')
        comment.update()
        return comment

    def delete_comment(self, id_: int) -> int:
        """
        Delete a comment by its ID.

        Args:
            id_ (int): The ID of the comment to delete.

        Returns:
            int: The ID of the deleted comment.
        """
        result = CommentModel.find_by_id(id_)
        if not result:
            raise ValueError('Comment not found')
        result.delete()
        return result.id

    def get_comment_by_id(self, id_: int) -> CommentModel:
        """
        Get a comment by its ID.

        Args:
            id_ (int): The ID of the comment to retrieve.

        Returns:
            CommentModel: The retrieved comment.
        """
        result = CommentModel.find_by_id(id_)
        if not result:
            raise ValueError('Comment not found')
        return result

    def get_user_comments(self, user_id: int) -> list[CommentModel]:
        """
        Get all comments for a specific user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list[CommentModel]: List of comments for the specified user.
        """
        if not UserModel.find_by_id(user_id):
            raise ValueError('User not found')
        return CommentModel.query.filter_by(user_id=user_id).all()

    def get_article_comments(self, article_id: int) -> list[CommentModel]:
        """
        Get all comments for a specific article.

        Args:
            article_id (int): The ID of the article.

        Returns:
            list[CommentModel]: List of comments for the specified article.
        """
        return CommentModel.query.filter_by(article_id=article_id).all()
