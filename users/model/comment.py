from sqlalchemy import Integer, String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from users.db.configuration import sa
from datetime import datetime
from typing import Any, Self


class CommentModel(sa.Model):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    content: Mapped[str] = mapped_column(String(1000))
    article_id: Mapped[int] = mapped_column(Integer(), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer(), ForeignKey('users.id'))

    created_at: Mapped[datetime] = mapped_column(insert_default=func.utc_timestamp())
    updated_at: Mapped[datetime] = mapped_column(default=func.utc_timestamp(), onupdate=func.utc_timestamp())

    def __eq__(self, other: Self) -> bool:
        return (
            self.id == other.id and
            self.article_id == other.article_id and
            self.user_id == other.user_id
        )

    def to_json(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'content': self.content,
            'article_id': self.article_id,
            'user_id': self.user_id,
        }

    def add(self) -> None:
        sa.session.add(self)
        sa.session.commit()

    def update(self) -> None:
        updated = sa.session.merge(self)
        sa.session.add(updated)
        sa.session.commit()

    def delete(self) -> None:
        sa.session.delete(self)
        sa.session.commit()

    @classmethod
    def find_by_id(cls, id_: int) -> Self | None:
        return sa.session.query(CommentModel).filter_by(id=id_).first()

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        return CommentModel(**data)
