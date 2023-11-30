from sqlalchemy import Integer, String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from users.db.configuration import sa
from datetime import datetime
from typing import Any, Self


class CommentModel(sa.Model):
    """
    CommentModel Class

    A SQLAlchemy Model class for the 'comments' table.

    Attributes:
        id (int): Primary key column representing the comment ID.
        content (str): Column representing the content of the comment.
        article_id (int): Column representing the ID of the associated article.
        user_id (int): Column representing the ID of the user who created the comment.
        created_at (datetime): Column representing the creation timestamp of the comment.
        updated_at (datetime): Column representing the last update timestamp of the comment.
    """
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    content: Mapped[str] = mapped_column(String(1000))
    article_id: Mapped[int] = mapped_column(Integer(), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer(), ForeignKey('users.id'))

    created_at: Mapped[datetime] = mapped_column(insert_default=func.utc_timestamp())
    updated_at: Mapped[datetime] = mapped_column(default=func.utc_timestamp(), onupdate=func.utc_timestamp())

    def __eq__(self, other: Self) -> bool:
        """
        Check if two CommentModel instances are equal.

        Args:
            other (CommentModel): The other CommentModel instance to compare.

        Returns:
            bool: True if instances are equal, False otherwise.
        """
        return (
            self.id == other.id and
            self.article_id == other.article_id and
            self.user_id == other.user_id
        )

    def to_json(self) -> dict[str, Any]:
        """
        Convert the CommentModel instance to a JSON-compatible dictionary.

        Returns:
            dict[str, Any]: JSON-compatible dictionary representing the CommentModel instance.
        """
        return {
            'id': self.id,
            'content': self.content,
            'article_id': self.article_id,
            'user_id': self.user_id,
        }

    def add(self) -> None:
        """Add the CommentModel instance to the session and commit the changes."""
        sa.session.add(self)
        sa.session.commit()

    def update(self) -> None:
        """Merge and update the CommentModel instance in the session and commit the changes."""
        updated = sa.session.merge(self)
        sa.session.add(updated)
        sa.session.commit()

    def delete(self) -> None:
        """Delete the CommentModel instance from the session and commit the changes."""
        sa.session.delete(self)
        sa.session.commit()

    @classmethod
    def find_by_id(cls, id_: int) -> Self | None:
        """
        Find a CommentModel instance by ID.

        Args:
            id_ (int): The ID to search for.

        Returns:
            CommentModel | None: The found CommentModel instance or None if not found.
        """
        return sa.session.query(CommentModel).filter_by(id=id_).first()

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        """
        Create a CommentModel instance from a JSON-compatible dictionary.

        Args:
            data (dict[str, Any]): JSON-compatible dictionary representing the CommentModel instance.

        Returns:
            CommentModel: The created CommentModel instance.
        """
        return CommentModel(**data)
