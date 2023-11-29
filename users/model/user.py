from users.security.configuration import bcrypt
from sqlalchemy import Integer, String, Boolean, func, Enum
from sqlalchemy.orm import Mapped, mapped_column
from users.db.configuration import sa
from typing import Literal, get_args
from datetime import datetime
from typing import Any, Self


UserRole = Literal['user', 'redactor', 'translator', 'admin']


class UserModel(sa.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)

    role: Mapped[UserRole] = mapped_column(Enum(
        *get_args(UserRole),
        name="user_role",
        create_constraint=True,
        validate_strings=True,
    ), default='user')

    created_at: Mapped[datetime] = mapped_column(insert_default=func.utc_timestamp())
    updated_at: Mapped[datetime] = mapped_column(default=func.utc_timestamp(), onupdate=func.utc_timestamp())

    def to_json(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
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

    def set_active(self) -> None:
        self.is_active = True
        sa.session.commit()

    def check_password(self, password: str) -> None:
        return bcrypt.check_password_hash(self.password, password)

    @classmethod
    def find_by_id(cls, id_: int) -> Self | None:
        return sa.session.query(UserModel).filter_by(id=id_).first()

    @classmethod
    def find_by_username(cls, username: str) -> Self | None:
        return sa.session.query(UserModel).filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email: str) -> Self | None:
        return sa.session.query(UserModel).filter_by(email=email).first()

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        hashed_passowrd = bcrypt.generate_password_hash(data.get('password')).decode('utf8')
        return UserModel(**data | {'password': hashed_passowrd})
