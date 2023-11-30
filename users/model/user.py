from users.security.configuration import bcrypt
from sqlalchemy import Integer, String, Boolean, func, Enum
from sqlalchemy.orm import Mapped, mapped_column
from users.db.configuration import sa
from typing import Literal, get_args
from datetime import datetime
from typing import Any, Self


UserRole = Literal['user', 'redactor', 'translator', 'admin']


class UserModel(sa.Model):
    """
    SQLAlchemy model representing the 'users' table.

    Attributes:
        id (int): Primary key for the user.
        username (str): User's username.
        email (str): User's email address.
        password (str): Hashed password using bcrypt.
        is_active (bool): Flag indicating whether the user is active or not.
        role (UserRole): User's role, chosen from the predefined set of roles.
        created_at (datetime): Timestamp indicating when the user was created.
        updated_at (datetime): Timestamp indicating the last update to the user.
    """
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
        """
        Convert the UserModel instance to a JSON-compatible dictionary.

        Returns:
            dict[str, Any]: JSON-compatible dictionary representing the UserModel instance.
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
        }

    def add(self) -> None:
        """Add the UserModel instance to the session and commit the changes."""
        sa.session.add(self)
        sa.session.commit()

    def update(self) -> None:
        """Merge and update the UserModel instance in the session and commit the changes."""
        updated = sa.session.merge(self)
        sa.session.add(updated)
        sa.session.commit()

    def delete(self) -> None:
        """Delete the UserModel instance from the session and commit the changes."""
        sa.session.delete(self)
        sa.session.commit()

    def set_active(self) -> None:
        """Set the user's 'is_active' flag to True and commit the changes."""
        self.is_active = True
        sa.session.commit()

    def check_password(self, password: str) -> None:
        """
        Check if the provided password matches the hashed password of the user.

        Args:
            password (str): The password to check.

        Returns:
            bool: True if the passwords match, False otherwise.
        """
        return bcrypt.check_password_hash(self.password, password)

    @classmethod
    def find_by_id(cls, id_: int) -> Self | None:
        """
        Find a UserModel instance by ID.

        Args:
            id_ (int): The ID to search for.

        Returns:
            UserModel | None: The found UserModel instance or None if not found.
        """
        return sa.session.query(UserModel).filter_by(id=id_).first()

    @classmethod
    def find_by_username(cls, username: str) -> Self | None:
        """
        Find a UserModel instance by username.

        Args:
            username (str): The username to search for.

        Returns:
            UserModel | None: The found UserModel instance or None if not found.
        """
        return sa.session.query(UserModel).filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email: str) -> Self | None:
        """
        Find a UserModel instance by email address.

        Args:
            email (str): The email address to search for.

        Returns:
            UserModel | None: The found UserModel instance or None if not found.
        """
        return sa.session.query(UserModel).filter_by(email=email).first()

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        """
        Create a UserModel instance from a JSON-compatible dictionary.

        Args:
            data (dict[str, Any]): JSON-compatible dictionary representing the UserModel instance.

        Returns:
            UserModel: The created UserModel instance.
        """
        hashed_passowrd = bcrypt.generate_password_hash(data.get('password')).decode('utf8')
        return UserModel(**data | {'password': hashed_passowrd})
