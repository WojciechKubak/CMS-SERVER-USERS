from users.db.configuration import sa
from users.security.configuration import bcrypt
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from sqlalchemy import func, Enum
from datetime import datetime
from typing import Self, Literal, get_args

UserRole = Literal['user', 'redactor', 'translator', 'admin']


class UserModel(sa.Model):

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    username: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column((String()), nullable=False)
    password: Mapped[str] = mapped_column(String(), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=False)

    role: Mapped[UserRole] = mapped_column(Enum(
        *get_args(UserRole),
        name="user_role",
        create_constraint=True,
        validate_strings=True,
    ))

    created_at: Mapped[datetime] = mapped_column(insert_default=func.utc_timestamp())
    updated_at: Mapped[datetime] = mapped_column(default=func.utc_timestamp(), onupdate=func.utc_timestamp())

    def add_or_update(self) -> None:
        sa.session.merge(self)
        sa.session.commit()

    def delete(self) -> None:
        sa.session.delete(self)
        sa.session.commit()

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password, password)

    @classmethod
    def find_by_id(cls, id_: int) -> Self:
        return sa.session.query(UserModel).filter_by(id=id_).first()

    @classmethod
    def find_by_username(cls, username: str) -> Self:
        return sa.session.query(UserModel).filter_by(username=username).first()
