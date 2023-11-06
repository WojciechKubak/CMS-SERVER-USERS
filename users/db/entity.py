from sqlalchemy import Integer, String, Boolean, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from typing import Literal, get_args
from datetime import datetime
from typing import Any

Base = declarative_base()

UserRole = Literal['user', 'redactor', 'translator', 'admin']


class UserEntity(Base):
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
